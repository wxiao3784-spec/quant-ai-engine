import akshare as ak
import pandas as pd
from openai import OpenAI
import os

def run_analysis():
    # 1. 抓取数据 (GitHub 云端服务器直连，不会报错)
    df = ak.stock_zh_a_spot_em()
    df = df[df['总市值'] > 10000000000].head(5) # 筛选市值 > 100亿的前5只
    
    # 2. 调用 DeepSeek
    client = OpenAI(api_key=os.environ['DEEPSEEK_API_KEY'], base_url="https://api.deepseek.com")
    
    for _, row in df.iterrows():
        content = f"分析这只股票：{row['名称']}，PE:{row['市盈率-动态']}，总市值:{row['总市值']}。请用V7.0框架评分。"
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": content}]
        )
        print(f"--- {row['名称']} 评估报告 ---\n{response.choices[0].message.content}\n")

if __name__ == "__main__":
    run_analysis()
