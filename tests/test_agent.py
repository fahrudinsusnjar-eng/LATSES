from lat_ses import LatSesAgent


def test_agent_remembers_and_responds():
    agent = LatSesAgent(name="TestAgent")

    response = agent.respond("Summarize the constitution")

    assert "TestAgent" in response
    assert agent.memory[-1] == "Summarize the constitution"


def test_agent_plan_returns_steps():
    agent = LatSesAgent()

    steps = agent.plan("Write a specification")

    assert len(steps) == 3
    assert steps[0].startswith("1. Analyze")
