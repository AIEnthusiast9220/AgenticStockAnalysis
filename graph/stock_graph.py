from langgraph.graph import StateGraph
from agents.news_agent import analyze_news
from agents.trend_agent import analyze_trends
from agents.prediction_agent import predict_future
from typing import TypedDict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockState(TypedDict):
    stock: str
    news_result: dict
    trend_result: dict
    news: dict
    trend: dict
    prediction: dict

def run_stock_graph(stock):
    graph = StateGraph(state_schema=StockState)

    def run_parallel(state):
        logger.info("Running get_news and get_trend in parallel")
        return {
            "news_result": analyze_news(state["stock"]),
            "trend_result": analyze_trends(state["stock"])
        }

    def combine_results(state):
        logger.info("Combining results")
        return {
            "news": state["news_result"],
            "trend": state["trend_result"]
        }

    def predict_node(state):
        logger.info("Running prediction")
        return {
            "prediction": predict_future(state["stock"], state["news"], state["trend"])
        }

    # Node definitions
    graph.add_node("parallel", run_parallel)
    graph.add_node("combine", combine_results)
    graph.add_node("predict", predict_node)

    # Flow setup
    graph.set_entry_point("parallel")
    graph.add_edge("parallel", "combine")
    graph.add_edge("combine", "predict")
    graph.set_finish_point("predict")

    try:
        graph.compile().print_ascii()
    except Exception as e:
        logger.warning(f"Could not render LangGraph diagram: {e}")

    # Compile and visualize
    try:
        app = graph.compile()
        app.print_ascii()
    except Exception as e:
        logger.warning(f"Could not render LangGraph diagram: {e}")

    # Run the pipeline
    result = app.invoke({"stock": stock})
    return result
