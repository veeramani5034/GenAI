import streamlit as st
import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.retrievers import BM25Retriever
from tavily import TavilyClient
import warnings
import fitz  # PyMuPDF for image extraction
from PIL import Image
import io
import base64
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="AWS DynamoDB Doc Explorer", page_icon="🗄️", layout="wide")

# Initialize session state
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'vector_retriever' not in st.session_state:
    st.session_state.vector_retriever = None
if 'bm25_retriever' not in st.session_state:
    st.session_state.bm25_retriever = None
if 'documents' not in st.session_state:
    st.session_state.documents = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'images_processed' not in st.session_state:
    st.session_state.images_processed = False

def extract_images_from_pdf(pdf_path):
    """Extract images from PDF with their page numbers"""
    images = []
    try:
        pdf_document = fitz.open(pdf_path)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Convert to PIL Image
                image = Image.open(io.BytesIO(image_bytes))
                
                # Store image with metadata
                images.append({
                    "page": page_num + 1,
                    "image": image,
                    "image_bytes": image_bytes,
                    "index": img_index,
                    "id": f"img_page{page_num + 1}_idx{img_index}"
                })
        
        pdf_document.close()
        return images
    except Exception as e:
        st.error(f"Error extracting images: {str(e)}")
        return []

def describe_images_with_gpt4_vision(images, openai_api_key):
    """Use GPT-4 Vision to describe images"""
    descriptions = []
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_api_key)
        
        for img_data in images:
            # Convert PIL image to base64
            buffered = io.BytesIO()
            img_data["image"].save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Call GPT-4 Vision
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this image in detail. If it's a diagram, chart, timeline, or table, explain what it shows. Include any text, labels, or key information visible in the image."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            description = response.choices[0].message.content
            descriptions.append({
                "id": img_data["id"],
                "page": img_data["page"],
                "description": description,
                "image_bytes": img_data["image_bytes"]
            })
    
    except Exception as e:
        st.error(f"Error describing images: {str(e)}")
    
    return descriptions

def store_images_in_chroma(image_descriptions, vectorstore, embeddings):
    """Store image descriptions in Chroma vector store"""
    try:
        from langchain_core.documents import Document
        
        # Create documents from image descriptions
        image_docs = []
        for img_desc in image_descriptions:
            doc = Document(
                page_content=f"[IMAGE] {img_desc['description']}",
                metadata={
                    "type": "image",
                    "page": img_desc["page"],
                    "image_id": img_desc["id"],
                    "source": "pdf_image"
                }
            )
            image_docs.append(doc)
        
        # Add to existing vectorstore
        if image_docs:
            st.info(f"Storing {len(image_docs)} images in Chroma...")
            vectorstore.add_documents(image_docs)
            st.success(f"✅ Successfully stored {len(image_docs)} images in vector database")
            
        return True
    except Exception as e:
        st.error(f"Error storing images in Chroma: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return False

def save_images_locally(image_descriptions, output_dir="./pdf_images"):
    """Save extracted images locally for retrieval"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        for img_desc in image_descriptions:
            image_path = os.path.join(output_dir, f"{img_desc['id']}.png")
            
            # Save image
            image = Image.open(io.BytesIO(img_desc["image_bytes"]))
            image.save(image_path)
        
        return True
    except Exception as e:
        st.error(f"Error saving images: {str(e)}")
        return False

def load_image_from_disk(image_id, output_dir="./pdf_images"):
    """Load image from disk by ID"""
    try:
        image_path = os.path.join(output_dir, f"{image_id}.png")
        if os.path.exists(image_path):
            return Image.open(image_path)
        return None
    except Exception as e:
        return None

def load_and_process_pdf(pdf_path, openai_api_key=None, process_images=False, force_reprocess=False):
    """Load PDF and create vector store with BM25 reranking"""
    try:
        # Create embeddings using HuggingFace
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Check if Chroma DB already exists
        chroma_exists = os.path.exists("./chroma_db") and os.path.exists("./chroma_db/chroma.sqlite3")
        images_exist = os.path.exists("./pdf_images") and len(os.listdir("./pdf_images")) > 0
        
        if chroma_exists and not force_reprocess:
            # Load existing vectorstore
            vectorstore = Chroma(
                persist_directory="./chroma_db",
                embedding_function=embeddings
            )
            
            # Load PDF for BM25 retriever
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=300,
                length_function=len
            )
            splits = text_splitter.split_documents(documents)
            
            # Create retrievers - increase k to get more results including images
            vector_retriever = vectorstore.as_retriever(
                search_kwargs={"k": 15}  # Increased to ensure images are retrieved
            )
            bm25_retriever = BM25Retriever.from_documents(splits)
            bm25_retriever.k = 8
            
            # Count images
            image_count = len(os.listdir("./pdf_images")) if images_exist else 0
            
            return vectorstore, vector_retriever, bm25_retriever, splits, image_count
        
        # Process from scratch if not exists or force reprocess
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        # Split text using recursive character splitter with larger chunks for tables
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=300,
            length_function=len
        )
        splits = text_splitter.split_documents(documents)
        
        # Create Chroma vector store
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        
        # Process images if requested
        image_count = 0
        if process_images and openai_api_key:
            st.info("Starting image extraction...")
            # Extract images
            images = extract_images_from_pdf(pdf_path)
            st.info(f"Extracted {len(images)} images from PDF")
            
            if images:
                # Describe images with GPT-4 Vision
                st.info("Analyzing images with GPT-4 Vision...")
                image_descriptions = describe_images_with_gpt4_vision(images, openai_api_key)
                st.info(f"Generated descriptions for {len(image_descriptions)} images")
                
                # Save images to disk
                st.info("Saving images to disk...")
                save_images_locally(image_descriptions)
                
                # Store image descriptions in Chroma
                st.info("Storing image descriptions in vector database...")
                success = store_images_in_chroma(image_descriptions, vectorstore, embeddings)
                
                if success:
                    image_count = len(image_descriptions)
                    st.success(f"✅ Successfully processed {image_count} images")
                else:
                    st.error("Failed to store images in Chroma")
            else:
                st.warning("No images found in PDF")
        
        # Create retrievers with more results to include images
        vector_retriever = vectorstore.as_retriever(
            search_kwargs={"k": 15}  # Increased to ensure images are retrieved
        )
        bm25_retriever = BM25Retriever.from_documents(splits)
        bm25_retriever.k = 8
        
        # Return both retrievers for ensemble approach
        return vectorstore, vector_retriever, bm25_retriever, splits, image_count
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None, None, None, None, 0

def query_document(question, vector_retriever, bm25_retriever, llm):
    """Query the document using RAG with BM25 reranking"""
    try:
        # Get documents from vector retriever (includes both text and images)
        vector_docs = vector_retriever.invoke(question)
        
        # Get documents from BM25 (text only)
        bm25_docs = bm25_retriever.invoke(question)
        
        # Separate images from vector results
        image_docs = [doc for doc in vector_docs if doc.metadata.get("type") == "image"]
        text_vector_docs = [doc for doc in vector_docs if doc.metadata.get("type") != "image"]
        
        # Rerank images based on question keywords
        if image_docs:
            question_lower = question.lower()
            # Extract key terms from question
            key_terms = [word for word in question_lower.split() 
                        if word not in ['show', 'me', 'the', 'a', 'an', 'can', 'you', 'picture', 'image', 'diagram', 'figure']]
            
            # Score each image based on keyword matches
            scored_images = []
            for doc in image_docs:
                content_lower = doc.page_content.lower()
                # Count how many key terms appear in the description
                score = sum(1 for term in key_terms if term in content_lower)
                # Boost score if multiple words appear together
                if len(key_terms) >= 2:
                    phrase = ' '.join(key_terms[:3])  # Check first 3 words as phrase
                    if phrase in content_lower:
                        score += 5  # Big boost for phrase match
                scored_images.append((score, doc))
            
            # Sort by score descending
            scored_images.sort(key=lambda x: x[0], reverse=True)
            
            # Only keep images with score > 0 (at least one keyword match)
            image_docs = [doc for score, doc in scored_images if score > 0]
        
        # Combine and deduplicate text documents (simple ensemble)
        all_docs = []
        seen_content = set()
        
        # Add BM25 results first (keyword matching)
        for doc in bm25_docs:
            if doc.page_content not in seen_content:
                all_docs.append(doc)
                seen_content.add(doc.page_content)
        
        # Add vector text results (semantic matching)
        for doc in text_vector_docs:
            if doc.page_content not in seen_content:
                all_docs.append(doc)
                seen_content.add(doc.page_content)
        
        # Add top ranked images (limit to top 2 most relevant)
        all_docs.extend(image_docs[:2])
        
        if not all_docs or len(all_docs) == 0:
            return "NOT_FOUND_IN_DOCUMENT", []
        
        # Create context from retrieved documents (use top 6, excluding images for text context)
        text_docs_for_context = [doc for doc in all_docs if doc.metadata.get("type") != "image"][:6]
        context = "\n\n".join([doc.page_content for doc in text_docs_for_context])
        
        # If we have images, add their descriptions to context
        if image_docs:
            image_context = "\n\n".join([doc.page_content for doc in image_docs[:2]])
            context = f"{context}\n\n{image_context}" if context else image_context
        
        # Create prompt with strict instructions
        prompt = f"""You are a document assistant. Your ONLY job is to answer questions using the context provided below.

Context from document:
{context}

Question: {question}

CRITICAL RULES:
- You MUST ONLY use information from the context above
- DO NOT use your general knowledge or training data
- If the context does not contain information to answer the question, respond with EXACTLY: "NOT_FOUND_IN_DOCUMENT"
- If the context mentions the topic even briefly, provide that information
- DO NOT make up or infer information not present in the context

Answer:"""
        
        # Get response from LLM
        response = llm.invoke(prompt)
        answer = response.content if hasattr(response, 'content') else str(response)
        
        # Additional validation: check if answer contains keywords from context
        if answer and "NOT_FOUND_IN_DOCUMENT" not in answer:
            # Extract key terms from the question
            question_lower = question.lower()
            context_lower = context.lower()
            
            # Check if the answer topic is actually in the context
            # For questions about specific AWS services not in doc
            if any(term in question_lower for term in ['migration service', 'dms', 'rds', 's3', 'lambda', 'ec2']) and \
               not any(term in context_lower for term in ['migration', 'dms']):
                answer = "NOT_FOUND_IN_DOCUMENT"
        
        # Return all docs including images
        return answer, all_docs[:10]
    except Exception as e:
        return f"Error querying document: {str(e)}", []

def web_search_tavily(question, tavily_api_key):
    """Perform web search using Tavily API"""
    try:
        if not tavily_api_key:
            return None
        
        tavily_client = TavilyClient(api_key=tavily_api_key)
        response = tavily_client.search(query=question, max_results=3)
        
        if response and 'results' in response and len(response['results']) > 0:
            results_text = ""
            for idx, result in enumerate(response['results'][:3], 1):
                results_text += f"\n{idx}. {result.get('content', '')}\n"
                results_text += f"   Source: {result.get('url', '')}\n"
            return results_text
        else:
            return None
    except Exception as e:
        st.error(f"Web search error: {str(e)}")
        return None

# Streamlit UI
st.title("🗄️ AWS DynamoDB Doc Explorer")
st.markdown("Ask questions about AWS DynamoDB based on the documentation")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv('OPENAI_API_KEY', ''))
    tavily_api_key = st.text_input("Tavily API Key (for web search)", type="password", value=os.getenv('TAVILY_API_KEY', ''))
    
    if openai_api_key:
        os.environ['OPENAI_API_KEY'] = openai_api_key
    if tavily_api_key:
        os.environ['TAVILY_API_KEY'] = tavily_api_key
    
    st.markdown("---")
    st.markdown("### 📄 Document Status")
    
    # Diagnostic: Check what's in Chroma
    if st.session_state.vectorstore and st.button("Check Vector Store Contents"):
        try:
            # Query for all image documents
            test_results = st.session_state.vectorstore.similarity_search("image timeline diagram", k=20)
            image_count_in_db = sum(1 for doc in test_results if doc.metadata.get("type") == "image")
            st.info(f"Found {image_count_in_db} images in vector store out of {len(test_results)} total documents")
            
            # Show sample
            for doc in test_results[:5]:
                st.write(f"Type: {doc.metadata.get('type', 'text')}, Content preview: {doc.page_content[:100]}")
        except Exception as e:
            st.error(f"Error checking vector store: {str(e)}")
    
    # Auto-load PDF on first run
    if st.session_state.vectorstore is None and openai_api_key:
        # Check if already processed
        chroma_exists = os.path.exists("./chroma_db") and os.path.exists("./chroma_db/chroma.sqlite3")
        images_exist = os.path.exists("./pdf_images") and len(os.listdir("./pdf_images")) > 0
        
        if chroma_exists:
            st.warning("⚠️ Loading existing database - images may not be indexed. Click 'Reload PDF Document' to reprocess with images.")
            with st.spinner("Loading existing vector database..."):
                vectorstore, vector_retriever, bm25_retriever, documents, image_count = load_and_process_pdf(
                    "atc22-elhemali.pdf", 
                    openai_api_key=openai_api_key,
                    process_images=False,
                    force_reprocess=False
                )
                if vectorstore and vector_retriever and bm25_retriever:
                    st.session_state.vectorstore = vectorstore
                    st.session_state.vector_retriever = vector_retriever
                    st.session_state.bm25_retriever = bm25_retriever
                    st.session_state.documents = documents
                    st.session_state.images_processed = images_exist
                    st.info(f"✅ Loaded existing database! ({image_count} images found on disk)")
                else:
                    st.error("Failed to load vector database")
        else:
            st.info("🔄 No existing database found - processing PDF with images...")
            with st.spinner("Processing PDF document and extracting images..."):
                vectorstore, vector_retriever, bm25_retriever, documents, image_count = load_and_process_pdf(
                    "atc22-elhemali.pdf", 
                    openai_api_key=openai_api_key,
                    process_images=True,
                    force_reprocess=False
                )
                if vectorstore and vector_retriever and bm25_retriever:
                    st.session_state.vectorstore = vectorstore
                    st.session_state.vector_retriever = vector_retriever
                    st.session_state.bm25_retriever = bm25_retriever
                    st.session_state.documents = documents
                    st.session_state.images_processed = True
                    st.success(f"✅ PDF loaded successfully! Processed {image_count} images.")
                else:
                    st.error("Failed to load PDF")
    
    if st.session_state.vectorstore:
        st.success("✅ Document Ready")
        st.info(f"Total chunks: {len(st.session_state.documents) if st.session_state.documents else 0}")
        if st.session_state.images_processed:
            st.info("✅ Images indexed in vector store")
    
    if st.button("Reload PDF Document"):
        if not openai_api_key:
            st.error("Please provide OpenAI API Key")
        else:
            try:
                # Close existing vectorstore connection
                if st.session_state.vectorstore:
                    try:
                        st.session_state.vectorstore._client.reset()
                    except:
                        pass
                    st.session_state.vectorstore = None
                    st.session_state.vector_retriever = None
                    st.session_state.bm25_retriever = None
                    st.session_state.documents = None
                
                # Clear the old Chroma DB
                import shutil
                import time
                
                time.sleep(1)  # Give time for connections to close
                
                if os.path.exists("./chroma_db"):
                    try:
                        shutil.rmtree("./chroma_db")
                    except PermissionError:
                        st.error("Please close the app and manually delete the 'chroma_db' folder, then restart.")
                        st.stop()
                
                if os.path.exists("./pdf_images"):
                    shutil.rmtree("./pdf_images")
                
                with st.spinner("Reprocessing PDF and images from scratch..."):
                    vectorstore, vector_retriever, bm25_retriever, documents, image_count = load_and_process_pdf(
                        "atc22-elhemali.pdf",
                        openai_api_key=openai_api_key,
                        process_images=True,
                        force_reprocess=True
                    )
                    if vectorstore and vector_retriever and bm25_retriever:
                        st.session_state.vectorstore = vectorstore
                        st.session_state.vector_retriever = vector_retriever
                        st.session_state.bm25_retriever = bm25_retriever
                        st.session_state.documents = documents
                        st.session_state.images_processed = True
                        st.success(f"✅ PDF reloaded! Processed {image_count} images.")
                        st.rerun()
                    else:
                        st.error("Failed to load PDF")
            except Exception as e:
                st.error(f"Error during reload: {str(e)}")
                st.info("Please restart the app to reload the document.")
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main chat interface
if not openai_api_key:
    st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to get started.")
    st.info("The PDF document will be automatically loaded once you provide the API key.")
elif not st.session_state.vectorstore:
    st.info("⏳ Loading PDF document... Please wait.")
else:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if question := st.chat_input("Ask a question about your document..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.chat_history.append({"role": "user", "content": question})
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Initialize LLM with strict settings
                llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0,
                    openai_api_key=openai_api_key,
                    model_kwargs={"top_p": 0.1}  # More deterministic
                )
                
                # Debug: Test direct retrieval from vectorstore
                st.write("Debug: Testing direct vectorstore retrieval...")
                test_results = st.session_state.vectorstore.similarity_search(question, k=15)
                test_images = [doc for doc in test_results if doc.metadata.get("type") == "image"]
                st.write(f"Direct vectorstore search found {len(test_images)} images out of {len(test_results)} docs")
                
                # Query document (this will now retrieve both text and image descriptions from Chroma)
                answer, sources = query_document(question, st.session_state.vector_retriever, st.session_state.bm25_retriever, llm)
                
                # Debug: Show what was retrieved
                st.write(f"Debug: Retrieved {len(sources)} documents")
                for i, doc in enumerate(sources[:5]):
                    doc_type = doc.metadata.get("type", "text")
                    st.write(f"  {i+1}. Type: {doc_type}, Content: {doc.page_content[:80]}...")
                
                # Check if any retrieved sources are images
                image_sources = [doc for doc in sources if doc.metadata.get("type") == "image"]
                st.write(f"Debug: {len(image_sources)} are images")
                
                # Display images if found
                if image_sources:
                    st.markdown("### Found relevant image(s):")
                    for doc in image_sources:
                        image_id = doc.metadata.get("image_id")
                        page = doc.metadata.get("page")
                        
                        st.write(f"Debug: Loading image {image_id} from page {page}")
                        
                        # Load image from disk
                        image = load_image_from_disk(image_id)
                        if image:
                            st.image(image, caption=f"Page {page}", use_container_width=True)
                            # Extract description from document content (remove [IMAGE] prefix)
                            description = doc.page_content.replace("[IMAGE] ", "")
                            st.markdown(f"**Description:** {description}")
                            st.markdown("---")
                        else:
                            st.error(f"Could not load image {image_id} from disk")
                    
                    final_answer = f"I found {len(image_sources)} relevant image(s) from the document (shown above).\n\n"
                    if "NOT_FOUND_IN_DOCUMENT" not in answer:
                        final_answer += f"Additional context: {answer}"
                
                # Corrective RAG logic
                elif "NOT_FOUND_IN_DOCUMENT" in answer:
                    # Try alternative retrieval with more aggressive search
                    alt_vector_retriever = st.session_state.vectorstore.as_retriever(
                        search_kwargs={"k": 10}
                    )
                    st.session_state.bm25_retriever.k = 10
                    answer_corrective, sources_corrective = query_document(question, alt_vector_retriever, st.session_state.bm25_retriever, llm)
                    
                    # Check again for images in corrective retrieval
                    image_sources_corrective = [doc for doc in sources_corrective if doc.metadata.get("type") == "image"]
                    
                    if image_sources_corrective:
                        st.markdown("### Found relevant image(s):")
                        for doc in image_sources_corrective:
                            image_id = doc.metadata.get("image_id")
                            page = doc.metadata.get("page")
                            
                            image = load_image_from_disk(image_id)
                            if image:
                                st.image(image, caption=f"Page {page}", use_container_width=True)
                                description = doc.page_content.replace("[IMAGE] ", "")
                                st.markdown(f"**Description:** {description}")
                                st.markdown("---")
                        
                        final_answer = f"I found {len(image_sources_corrective)} relevant image(s) from the document (shown above)."
                    
                    # Reset BM25 k value
                    st.session_state.bm25_retriever.k = 6
                    
                    if "NOT_FOUND_IN_DOCUMENT" in answer_corrective and not image_sources_corrective:
                        # Perform web search using Tavily
                        st.warning("⚠️ Answer is not available in uploaded document, searching the web...")
                        web_result = web_search_tavily(question, tavily_api_key)
                        
                        if web_result:
                            final_answer = f"Based on web search:\n\n{web_result}"
                        else:
                            final_answer = "I couldn't find relevant information in the document or web. Please try rephrasing your question."
                    elif not image_sources_corrective:
                        final_answer = answer_corrective
                else:
                    final_answer = answer
                
                st.markdown(final_answer)
                st.session_state.chat_history.append({"role": "assistant", "content": final_answer})
