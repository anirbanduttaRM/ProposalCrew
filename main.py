import os
from dotenv import load_dotenv
from crew_agents import create_crew
from utils import read_rfp_txt, read_rfp_pdf, read_rfp_docx, export_to_ppt
from llm_caller import call_llm  # Import the refactored LLM caller

# Load environment variables
load_dotenv()

# ---- Read RFP from File ----
file_path = "rfp_docs/Sample_RFP_Document.pdf"  # Change to your file path

# ✅ Read RFP content based on file type
if file_path.endswith('.txt'):
    rfp_content = read_rfp_txt(file_path)
elif file_path.endswith('.pdf'):
    rfp_content = read_rfp_pdf(file_path)
elif file_path.endswith('.docx'):
    rfp_content = read_rfp_docx(file_path)
else:
    raise ValueError("Unsupported file format. Use .txt, .pdf, or .docx")

# ✅ Debugging: Print RFP content length
print(f"\n✅ RFP content length: {len(rfp_content)} characters")

# ---- LLM Generation Before CrewAI ----
print("\n🔥 Generating Initial Proposal with LLM...")

# ✅ Pass the model type as an argument
model_type = os.getenv("MODEL_TYPE", "huggingface").lower()  # Default to Hugging Face if not provided
print(f"\n🛠️ Using LLM Model: {model_type.upper()}")

# ✅ Call the LLM with the specified model type
initial_proposal = call_llm(f"Generate a proposal draft based on this RFP:\n\n{rfp_content}", model_type=model_type)

# ✅ Display the initial LLM proposal
print("\n💡 Initial LLM Proposal:")
print(initial_proposal)

# ✅ Create crew with tasks including the initial LLM-generated proposal
proposal_crew = create_crew(initial_proposal)

# ✅ Debugging: Print task details
print("\n🛠️ Task Details:")
for task in proposal_crew.tasks:
    print(f" - {task.name}: {task.expected_output}")

# ---- Run the Crew ----
print("\n🚀 Running CrewAI on LLM-generated Proposal...\n")

# ✅ Execute the crew
final_proposal = proposal_crew.kickoff()

print("\n📄 Final Proposal:\n")
print(final_proposal)

# ---- Export to PowerPoint ----
export_to_ppt(final_proposal, "Software_Proposal.pptx")
print("\n✅ Proposal exported to PowerPoint: 'Software_Proposal.pptx'")
