from crewai import Task
from agents import content_extractor, writer, reviewer

# Task 1: Extract RFP details
extract_task = Task(
    description="Extract all technical requirements, deadlines, and scoring criteria from the RFP.",
    expected_output="A detailed summary of RFP requirements and evaluation metrics.",
    agent=content_extractor
)

# Task 2: Write RFP Response
write_task = Task(
    description="Write a structured and persuasive RFP response based on the extracted details.",
    expected_output="A professional and detailed RFP response document.",
    agent=writer
)

# Task 3: Review the Response
review_task = Task(
    description="Review the RFP response for grammar, style, and technical accuracy.",
    expected_output="A refined, error-free, and polished final RFP response.",
    agent=reviewer
)