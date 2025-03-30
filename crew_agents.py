from crewai import Agent, Crew, Task

# ✅ Define agents (no LLM references here)
ProposalAnalyzer = Agent(
    name="ProposalAnalyzer",
    role="Software RFP Analyzer",
    goal="Analyze and summarize RFP details.",
    backstory="An experienced business analyst with expertise in evaluating software RFPs. Skilled at identifying key requirements, objectives, and potential risks.",
    verbose=True,
    memory=True
)

ProposalWriter = Agent(
    name="ProposalWriter",
    role="Proposal Writer",
    goal="Write a detailed and compelling proposal.",
    backstory="A seasoned technical writer with years of experience in crafting persuasive and detailed software development proposals.",
    verbose=True,
    memory=True
)

ProposalReviewer = Agent(
    name="ProposalReviewer",
    role="Proposal Reviewer",
    goal="Review and refine the proposal for quality.",
    backstory="A meticulous content reviewer with a keen eye for grammar, clarity, and compliance. Ensures the proposal is professional and error-free.",
    verbose=True,
    memory=True
)

# ✅ Define tasks and assign them to specific agents
def create_tasks(rfp_content):
    analyze_task = Task(
        name="Analyze RFP",
        description="Extract and summarize the key RFP requirements.",
        expected_output="Summary of RFP objectives, goals, and requirements.",
        input={"rfp_content": rfp_content},
        agent=ProposalAnalyzer  # Assign task to the agent
    )

    write_task = Task(
        name="Write Proposal",
        description="Draft a compelling and detailed proposal based on the RFP analysis.",
        expected_output="Complete proposal draft.",
        input={"rfp_content": rfp_content},
        agent=ProposalWriter  # Assign task to the agent
    )

    review_task = Task(
        name="Review Proposal",
        description="Proofread and refine the proposal for quality and compliance.",
        expected_output="Reviewed and polished proposal.",
        input={"rfp_content": rfp_content},
        agent=ProposalReviewer  # Assign task to the agent
    )

    return [analyze_task, write_task, review_task]

# ✅ Define the crew with agents and their assigned tasks
def create_crew(rfp_content):
    tasks = create_tasks(rfp_content)

    proposal_crew = Crew(
        agents=[ProposalAnalyzer, ProposalWriter, ProposalReviewer],
        tasks=tasks,  # Assign tasks linked with agents
        verbose=True
    )

    return proposal_crew
