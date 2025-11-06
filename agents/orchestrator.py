from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from agents.issue_detector import IssueDetectorAgent
from agents.action_planner import ActionPlannerAgent
from agents.notification_agent import NotificationAgent

class AgentState(TypedDict):
    image_path: str
    audio_text: str
    reporter_name: str
    location: str
    latitude: float
    longitude: float
    issue_detected: bool
    issue_type: str
    severity: str
    description: str
    confidence: float
    suggested_actions: dict
    agency_data: dict
    notification_sent: bool
    error: str

class CivicAgentOrchestrator:
    def __init__(self):
        self.detector = IssueDetectorAgent()
        self.planner = ActionPlannerAgent()
        self.notifier = NotificationAgent()
        self.workflow = self._build_workflow()
        
    def _build_workflow(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("detect_issue", self.detect_issue_node)
        workflow.add_node("plan_actions", self.plan_actions_node)
        workflow.add_node("route_notification", self.route_notification_node)
        workflow.add_node("send_notification", self.send_notification_node)
        
        workflow.set_entry_point("detect_issue")
        
        workflow.add_conditional_edges(
            "detect_issue",
            self.should_continue_after_detection,
            {
                "continue": "plan_actions",
                "end": END
            }
        )
        
        workflow.add_edge("plan_actions", "route_notification")
        workflow.add_edge("route_notification", "send_notification")
        workflow.add_edge("send_notification", END)
        
        return workflow.compile()
    
    def detect_issue_node(self, state: AgentState) -> AgentState:
        result = self.detector.detect_issue(state["image_path"], state.get("audio_text"))
        
        state["issue_detected"] = result["issue_detected"]
        state["issue_type"] = result["issue_type"]
        state["severity"] = result["severity"]
        state["description"] = result["description"]
        state["confidence"] = result["confidence"]
        
        return state
    
    def plan_actions_node(self, state: AgentState) -> AgentState:
        actions = self.planner.suggest_actions(
            state["issue_type"],
            state["description"],
            state["severity"]
        )
        
        state["suggested_actions"] = actions
        return state
    
    def route_notification_node(self, state: AgentState) -> AgentState:
        agency = self.notifier.route_to_agency(state["issue_type"])
        state["agency_data"] = agency
        return state
    
    def send_notification_node(self, state: AgentState) -> AgentState:
        if state["agency_data"]:
            issue_data = {
                "reporter_name": state["reporter_name"],
                "location": state["location"],
                "issue_type": state["issue_type"],
                "description": state["description"],
                "severity": state["severity"]
            }
            
            message = self.notifier.generate_notification(issue_data)
            # Note: issue_id would be set after DB save in FastAPI
            state["notification_sent"] = True
        
        return state
    
    def should_continue_after_detection(self, state: AgentState) -> str:
        if state["issue_detected"] and state["confidence"] > 0.5:
            return "continue"
        return "end"
    
    def process(self, initial_state: AgentState) -> AgentState:
        """Execute the full workflow"""
        result = self.workflow.invoke(initial_state)
        return result