from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient

class AINewsNode:
    def __init__(self , model):
        self.llm = model
        self.tavily = TavilyClient()
        self.state = {}

    def fetch_news(self , state : dict) -> dict:
        """
        Fetch AI News Based on the specified frequency.

        Args : 
            state (dict) : the state dictionary containing 'frequency'.

        Returns :
            dict : Updated State with 'news_data' key containing fetched news
        """

        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {"daily" : 'd' , "weekly" : "w" , "monthly" : "m" , "year" : "y"}
        days_map = {"daily" : 1 , "weekly" : 7 , "monthly" : 30 , "year" : 366}
        response = self.tavily.search(
            query="Top Artificial Intelligence (AI) technology news USA and globally",
            topic = "news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days = days_map[frequency]
        )
        state['news_data'] = response.get("results", [])
        self.state['news_data'] = state['news_data']
        return state
    
    def summarizing_result(self , state: dict) -> dict:
        """
        Summarize the fetched News using LLM 

        Args : 
            state (dict) : The state dictionary containing the 'news_data'

        Returns : 
            dict : Updated state with 'summary' key containing the summarized News
        """

        news_items= self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages(
           [ ('system' , """Summarize AI news articles into markdown format. For each item include:
                        - Date in **YYYY-MM-DD** format in IST timezone
                        - Concise sentences summary from latest news
                        - Sort news by date wise (latest first)
                        - Source URL as link
                        Use format:
                        ### [Date]
                        - [Summary](URL)"""),
            ('human' , "Articles : \n {articles}")]
        )
        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles = articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state

    def save_results(self , state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency.lower()}_summary.md"
        with open(filename , 'w') as f:
            f.write(f"# {frequency.capitalize()} AI NEWS \n\n")
            f.write(summary)


        self.state['filename'] = filename
        return self.state