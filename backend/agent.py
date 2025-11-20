"""
AI Agent using Google's Agent Development Kit (ADK)
Following the official ADK structure: https://google.github.io/adk-docs/get-started/quickstart/
"""
import pandas as pd
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Load environment variables
load_dotenv()

# Global session service to maintain conversation history across queries
_global_session_service = None

def get_session_service():
    """Get or create the global session service"""
    global _global_session_service
    if _global_session_service is None:
        from google.adk.sessions import InMemorySessionService
        _global_session_service = InMemorySessionService()
    return _global_session_service


def create_dataframe_tools(df: pd.DataFrame):
    """
    Create tool functions for dataframe operations.
    These functions are wrapped with FunctionTool as per ADK documentation.
    """
    
    def calculate_mean(column: str) -> Dict[str, Any]:
        """Calculate the mean/average of a numeric column in the dataframe.
        
        Args:
            column (str): The name of the column to calculate mean for.
            
        Returns:
            dict: Result with mean value and message.
        """
        try:
            mean_value = float(df[column].mean())
            return {
                "status": "success",
                "result": mean_value,
                "message": f"Mean of {column}: {mean_value:.2f}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error_message": f"Error calculating mean: {str(e)}"
            }
    
    def calculate_median(column: str) -> Dict[str, Any]:
        """Calculate the median of a numeric column.
        
        Args:
            column (str): The name of the column to calculate median for.
            
        Returns:
            dict: Result with median value and message.
        """
        try:
            median_value = float(df[column].median())
            return {
                "status": "success",
                "result": median_value,
                "message": f"Median of {column}: {median_value:.2f}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error_message": f"Error calculating median: {str(e)}"
            }
    
    def sum_column(column: str, filter_column: Optional[str] = None, filter_value: Optional[str] = None) -> Dict[str, Any]:
        """Calculate the sum of a numeric column, optionally filtered by conditions.
        
        Args:
            column (str): The name of the column to sum.
            filter_column (str, optional): Column to filter by.
            filter_value (str, optional): Value to filter for.
            
        Returns:
            dict: Result with sum value and message.
        """
        try:
            if filter_column and filter_value:
                filtered_df = df[df[filter_column] == filter_value]
                sum_value = float(filtered_df[column].sum())
                message = f"Sum of {column} where {filter_column} = {filter_value}: {sum_value:.2f}"
            else:
                sum_value = float(df[column].sum())
                message = f"Sum of {column}: {sum_value:.2f}"
            
            return {
                "status": "success",
                "result": sum_value,
                "message": message
            }
        except Exception as e:
            return {
                "status": "error",
                "error_message": f"Error calculating sum: {str(e)}"
            }
    
    def filter_by_date_range(date_column: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """Filter the dataframe by a date range.
        
        Args:
            date_column (str): The name of the date column.
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.
            
        Returns:
            dict: Result with filtered data count and records.
        """
        try:
            filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
            count = len(filtered_df)
            return {
                "status": "success",
                "result": count,
                "filtered_records": filtered_df.to_dict('records'),
                "message": f"Found {count} records in the date range from {start_date} to {end_date}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error_message": f"Error filtering by date range: {str(e)}"
            }
    
    def get_dataframe_info() -> Dict[str, Any]:
        """Get basic information about the dataframe including columns, shape, and data types.
        
        Returns:
            dict: Result with dataframe information.
        """
        try:
            return {
                "status": "success",
                "result": {
                    "columns": list(df.columns),
                    "rows": len(df),
                    "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                    "sample_data": df.head(5).to_dict('records')
                },
                "message": f"Dataframe has {len(df)} rows and {len(df.columns)} columns: {', '.join(df.columns)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error_message": f"Error getting dataframe info: {str(e)}"
            }
    
    def get_available_capabilities() -> Dict[str, Any]:
        """Get information about what this agent can help with and available tools.
        Use this tool when users ask general questions like 'what can you help me with', 
        'what can you do', 'how can you help', or similar queries about capabilities.
        
        Returns:
            dict: Information about agent capabilities and available tools.
        """
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        all_cols = df.columns.tolist()
        
        capabilities = {
            "status": "success",
            "agent_type": "CSV Data Analysis Agent",
            "capabilities": [
                "Calculate statistical measures (mean, median, sum) for numeric columns",
                "Filter data by date ranges or specific conditions",
                "Aggregate data (sum, mean, count, max, min) with filters",
                "Group data by time periods (month, year) or categories and aggregate",
                "Provide information about the dataset structure and columns",
                "Answer questions about the uploaded CSV data"
            ],
            "available_tools": [
                "calculate_mean - Calculate average of numeric columns",
                "calculate_median - Calculate median of numeric columns",
                "sum_column - Calculate sum of numeric columns (with optional filters)",
                "filter_by_date_range - Filter data by date ranges",
                "filter_and_aggregate - Filter and aggregate data in one operation",
                "group_by_and_aggregate - Group by month/category and aggregate (e.g., sales by month)",
                "get_dataframe_info - Get dataset structure and sample data"
            ],
            "dataset_info": {
                "total_rows": len(df),
                "total_columns": len(all_cols),
                "numeric_columns": numeric_cols,
                "all_columns": all_cols
            },
            "message": "I am a specialized CSV Data Analysis Agent. I can help you analyze your uploaded CSV data using various statistical and filtering tools."
        }
        return capabilities
    
    def group_by_and_aggregate(group_column: str, aggregate_column: str, aggregation: str = "sum") -> Dict[str, Any]:
        """Group data by a column (e.g., month, category) and aggregate another column.
        Use this for queries like "sales by month", "revenue by category", "units sold by month", etc.
        
        Args:
            group_column (str): Column to group by (e.g., "Month", "Category", or date column name).
            aggregate_column (str): Column to aggregate (e.g., "Units_Sold", "sales", "revenue").
            aggregation (str): Type of aggregation: 'sum', 'mean', 'count', 'max', or 'min'. Default is 'sum'.
            
        Returns:
            dict: Result with grouped and aggregated data.
        """
        try:
            # Normalize column names (case-insensitive matching)
            group_col = None
            agg_col = None
            
            for col in df.columns:
                if col.lower() == group_column.lower():
                    group_col = col
                if col.lower() == aggregate_column.lower():
                    agg_col = col
            
            if group_col is None:
                return {
                    "status": "error",
                    "error_message": f"Column '{group_column}' not found. Available columns: {', '.join(df.columns)}"
                }
            
            if agg_col is None:
                return {
                    "status": "error",
                    "error_message": f"Column '{aggregate_column}' not found. Available columns: {', '.join(df.columns)}"
                }
            
            # Perform grouping and aggregation
            if aggregation not in ['sum', 'mean', 'count', 'max', 'min']:
                return {
                    "status": "error",
                    "error_message": f"Invalid aggregation type. Must be one of: sum, mean, count, max, min"
                }
            
            # Group by the column and aggregate
            grouped = df.groupby(group_col)[agg_col]
            aggregated = getattr(grouped, aggregation)()
            
            # Convert to list of dictionaries for better readability
            grouped_data = []
            for group_value, agg_value in aggregated.items():
                grouped_data.append({
                    group_col: str(group_value),
                    f"{aggregation}_{agg_col}": float(agg_value) if pd.notna(agg_value) else 0
                })
            
            result = {
                "status": "success",
                "result": aggregated.to_dict(),
                "message": f"{aggregation.capitalize()} of {agg_col} grouped by {group_col}",
                "grouped_data": grouped_data,
                "summary": f"Found {len(grouped_data)} groups"
            }
            
            return result
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return {
                "status": "error",
                "error_message": f"Error in group by and aggregate: {str(e)}",
                "debug": error_details[:500] if len(error_details) > 500 else error_details
            }
    
    def filter_and_aggregate(filter_column: str, filter_value: str, aggregate_column: str, aggregation: str) -> Dict[str, Any]:
        """Filter dataframe by a condition and then aggregate (sum, mean, count, max, min) a column.
        
        Args:
            filter_column (str): Column to filter by.
            filter_value (str): Value to filter for.
            aggregate_column (str): Column to aggregate.
            aggregation (str): Type of aggregation: 'sum', 'mean', 'count', 'max', or 'min'.
            
        Returns:
            dict: Result with aggregated value and message.
        """
        try:
            filtered_df = df[df[filter_column] == filter_value]
            if len(filtered_df) == 0:
                return {
                    "status": "error",
                    "error_message": f"No records found where {filter_column} = {filter_value}"
                }
            
            if aggregation not in ['sum', 'mean', 'count', 'max', 'min']:
                return {
                    "status": "error",
                    "error_message": f"Invalid aggregation type. Must be one of: sum, mean, count, max, min"
                }
            
            aggregated_value = float(getattr(filtered_df[aggregate_column], aggregation)())
            
            return {
                "status": "success",
                "result": aggregated_value,
                "message": f"{aggregation.capitalize()} of {aggregate_column} where {filter_column} = {filter_value}: {aggregated_value:.2f}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error_message": f"Error in filter and aggregate: {str(e)}"
            }
    
    # Return list of FunctionTool instances (wrapping functions as per ADK documentation)
    return [
        FunctionTool(func=calculate_mean),
        FunctionTool(func=calculate_median),
        FunctionTool(func=sum_column),
        FunctionTool(func=filter_by_date_range),
        FunctionTool(func=get_dataframe_info),
        FunctionTool(func=filter_and_aggregate),
        FunctionTool(func=group_by_and_aggregate),
        FunctionTool(func=get_available_capabilities)
    ]


def create_agent(df: pd.DataFrame, model_name: str = "gemini-2.0-flash") -> Agent:
    """
    Create a root agent using ADK's Agent class.
    Following the structure from: https://google.github.io/adk-docs/get-started/quickstart/
    
    Args:
        df (pd.DataFrame): The dataframe to create tools for.
        model_name (str): The model to use (default: gemini-2.0-flash-exp).
        
    Returns:
        Agent: The ADK Agent instance.
    """
    # Get dataframe info for context
    df_info = {
        "columns": list(df.columns),
        "rows": len(df),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "sample_data": df.head(5).to_dict('records')
    }
    
    # Create tools
    tools = create_dataframe_tools(df)
    
    # Create system instruction with dataframe context and guardrails
    instruction = f"""You are a specialized CSV Data Analysis Agent. Your primary role is to help users analyze their uploaded CSV data.

**IMPORTANT GUARDRAILS:**
- You are ONLY a data analysis agent for CSV files. You cannot help with general questions outside of data analysis.
- If users ask about topics unrelated to data analysis (e.g., weather, news, general knowledge), politely redirect them: "I'm a CSV Data Analysis Agent. I can only help you analyze your uploaded CSV data. Please ask me questions about your dataset."
- Always stay focused on the uploaded CSV data and its analysis.

**YOUR IDENTITY:**
- You are a CSV Data Analysis Agent
- You help users understand and analyze their CSV data
- You have access to specialized tools for data analysis

**WHEN TO USE WHICH TOOL:**

1. **General Questions** (e.g., "what can you help with", "what can you do", "how can you help"):
   - Use 'get_available_capabilities' tool to provide comprehensive information about your capabilities

2. **Statistical Questions** (e.g., "what is the average", "mean of X", "median"):
   - Use 'calculate_mean' for averages/means
   - Use 'calculate_median' for medians

3. **Sum/Total Questions** (e.g., "total sales", "sum of revenue"):
   - Use 'sum_column' tool
   - If filtering is needed, provide filter_column and filter_value parameters

4. **Date Range Questions** (e.g., "sales in January", "data from 2024"):
   - Use 'filter_by_date_range' tool
   - Identify the date column and extract start/end dates from the query

5. **Complex Filtering + Aggregation** (e.g., "average sales for product A", "total revenue where status is active"):
   - Use 'filter_and_aggregate' tool
   - Identify: filter_column, filter_value, aggregate_column, and aggregation type (sum/mean/count/max/min)

6. **Grouping by Time Period or Category** (e.g., "sales by month", "revenue by category", "units sold by month"):
   - Use 'group_by_and_aggregate' tool
   - For "by month" queries: 
     * If there's a "Month" column, use that as group_column
     * If there's a date column, the tool can extract months from it
     * aggregate_column is the metric to aggregate (e.g., Units_Sold, sales, revenue)
   - The tool performs case-insensitive column matching
   - Identify: group_column (Month, Category, or date column), aggregate_column (metric to sum/aggregate), and aggregation type (default: sum)
   - Example: "units sold by month" → group_column="Month", aggregate_column="Units_Sold", aggregation="sum"

7. **Dataset Information** (e.g., "what columns are there", "show me the data structure"):
   - Use 'get_dataframe_info' tool

8. **Tabular Output Requests** (e.g., "show me the data", "give me a table"):
   - Use 'get_dataframe_info' to get sample data, or explain that you can provide filtered/aggregated results

**DataFrame Information:**
- Columns: {', '.join(df.columns)}
- Number of rows: {len(df)}
- Data types: {df_info['dtypes']}
- Sample data: {df_info['sample_data']}

**RESPONSE GUIDELINES:**
- Always be helpful and clear
- When providing numerical results, include context and units if applicable
- If a tool returns an error, explain what went wrong and suggest alternatives
- For tabular data requests, format responses clearly or use the appropriate tool to get structured data
- Always reference the specific columns and data from the user's CSV file
- **BE PROACTIVE**: Don't ask follow-up questions if you can infer the answer from context
- **INFER COLUMN NAMES**: If a user mentions a metric (e.g., "units sold", "sales", "revenue"), look for matching or similar column names in the dataset
- **EXECUTE IMMEDIATELY**: When a user provides a clear request (e.g., "mean" after mentioning "units sold"), immediately use the appropriate tool with the inferred column name
- **CONTEXT AWARENESS**: Remember previous parts of the conversation. If a user says "units sold" and then "mean", they want the mean of the "units sold" column

**TOOL SELECTION STRATEGY:**
- Analyze the user's question carefully
- Identify keywords that indicate which tool to use (mean/average → calculate_mean, sum/total → sum_column, etc.)
- **INFER COLUMN NAMES FROM CONTEXT**: 
  - If user mentions "units sold" → look for columns like "units_sold", "units", "Units Sold", etc.
  - If user mentions "sales" → look for "sales", "Sales", "total_sales", etc.
  - Use partial matching and case-insensitive matching
  - If multiple matches exist, use the most likely one or ask for clarification only if truly ambiguous
- If the question involves filtering AND aggregation, use filter_and_aggregate
- **AVOID UNNECESSARY QUESTIONS**: If you can reasonably infer what the user wants, just do it. Only ask questions if the request is truly ambiguous.
- If unsure about data structure, start with get_dataframe_info to understand the data structure first
- For general capability questions, always use get_available_capabilities

**CONVERSATION FLOW:**
- **MAINTAIN CONTEXT**: Remember the conversation history. If you previously asked about "units sold" and the user responds with just "mean", they want the mean of units_sold. Don't ask again.
- When user provides a metric name and then a calculation type (e.g., "units sold" → "mean"), immediately execute the calculation
- **SHORT RESPONSES**: If a user gives a short answer like "mean", "sum", "average", look at the conversation history to see what was being discussed
- Don't ask "which column?" if the column name was already mentioned or can be inferred from context
- Be smart about matching: "units sold" matches "Units_Sold", "units_sold", "Units Sold", "units", etc.
- **INFER FROM PREVIOUS MESSAGES**: If the conversation mentions a column name, use that context for subsequent short answers
- If you need to ask a question, make it specific and actionable, not generic
- **BE PROACTIVE**: When in doubt, try to infer and execute. Only ask if truly necessary."""
    
    # Create the root agent using ADK's Agent class
    root_agent = Agent(
        name="dataframe_analysis_agent",
        model=model_name,
        description="Agent to answer questions about data in a pandas DataFrame using various analysis tools.",
        instruction=instruction,
        tools=tools,
    )
    
    return root_agent


async def process_query(agent: Agent, query: str, df: pd.DataFrame, session_id: str = None) -> str:
    """
    Process a query using the ADK agent.
    Uses the Runner class with InMemorySessionService as per ADK documentation.
    
    Args:
        agent (Agent): The ADK Agent instance.
        query (str): The user's query.
        df (pd.DataFrame): The dataframe (for backward compatibility).
        session_id (str, optional): Session ID to maintain conversation context.
        
    Returns:
        str: The agent's response.
    """
    try:
        from google.adk import Runner
        from google.genai import types as genai_types
        import uuid
        
        # Use shared session service to maintain conversation history
        session_service = get_session_service()
        
        # Create an App to wrap the agent (ADK requires this for proper execution)
        # Use "agents" as app_name to match ADK's internal directory structure expectations
        from google.adk import apps
        app = apps.App(
            name="agents",  # Must match the directory where agents are loaded from
            root_agent=agent
        )
        
        # Create a runner with the app
        runner = Runner(app=app, session_service=session_service)
        
        # Use the provided session_id to maintain conversation context
        # This ensures conversation history is preserved across queries
        if session_id is None:
            # Fallback: create a session ID if not provided
            import hashlib
            df_hash = hashlib.md5(str(df.columns.tolist()).encode()).hexdigest()[:8]
            session_id = f"session_{df_hash}"
        
        user_id = "user"
        
        # Create the message content
        message = genai_types.Content(
            role="user",
            parts=[genai_types.Part(text=query)]
        )
        
        # Get or create the session (required by ADK)
        # get_session returns None if session doesn't exist (doesn't raise exception)
        existing_session = await session_service.get_session(
            app_name="agents",
            user_id=user_id,
            session_id=session_id
        )
        
        # Create session if it doesn't exist (None means it doesn't exist)
        if existing_session is None:
            try:
                await session_service.create_session(
                    app_name="agents",
                    user_id=user_id,
                    session_id=session_id
                )
            except Exception as create_error:
                # If creation fails with "already exists", another request created it concurrently
                # Try to get it one more time
                if "already exists" in str(create_error).lower() or "exists" in str(create_error).lower():
                    existing_session = await session_service.get_session(
                        app_name="agents",
                        user_id=user_id,
                        session_id=session_id
                    )
                    if existing_session is None:
                        raise Exception(f"Session creation reported 'already exists' but get_session still returns None")
                else:
                    # Some other error during creation
                    raise create_error
        
        # Run the agent and collect events
        response_text = None
        response_parts = []
        
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):
            # Look for text response in events
            # ADK events can have different structures, so we check multiple attributes
            event_text = None
            
            if hasattr(event, 'text'):
                event_text = event.text
            elif hasattr(event, 'content'):
                if isinstance(event.content, str):
                    event_text = event.content
                elif hasattr(event.content, 'text'):
                    event_text = event.content.text
                elif hasattr(event.content, 'parts'):
                    # Content might have parts with text
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            event_text = part.text
                            break
            elif hasattr(event, 'message'):
                if hasattr(event.message, 'text'):
                    event_text = event.message.text
                elif hasattr(event.message, 'content'):
                    if isinstance(event.message.content, str):
                        event_text = event.message.content
                    elif hasattr(event.message.content, 'text'):
                        event_text = event.message.content.text
            
            # Collect all text parts
            if event_text:
                response_parts.append(event_text)
                response_text = event_text  # Keep the last one, or we'll join all
        
        # Join all response parts if we collected multiple
        if response_parts:
            response_text = '\n'.join(response_parts) if len(response_parts) > 1 else response_parts[0]
        
        if response_text:
            return response_text
        else:
            return "I received your query but couldn't generate a response. Please try rephrasing your question."
            
    except Exception as e:
        # Fallback to simple pandas operations for common queries
        query_lower = query.lower()
        
        if "mean" in query_lower or "average" in query_lower:
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                results = []
                for col in numeric_cols:
                    if col.lower() in query_lower or len(numeric_cols) == 1:
                        results.append(f"Mean of {col}: {df[col].mean():.2f}")
                if results:
                    return "\n".join(results)
        
        if "sum" in query_lower or "total" in query_lower:
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                results = []
                for col in numeric_cols:
                    if col.lower() in query_lower or "sales" in query_lower or "revenue" in query_lower or len(numeric_cols) == 1:
                        results.append(f"Sum of {col}: {df[col].sum():.2f}")
                if results:
                    return "\n".join(results)
        
        if "columns" in query_lower or "column" in query_lower:
            return f"The dataset has {len(df.columns)} columns: {', '.join(df.columns)}"
        
        return f"I encountered an error processing your query: {str(e)}. Please try rephrasing your question or check if the data contains the columns you're asking about."
