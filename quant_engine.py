import akshare as ak
import pandas as pd

def value_invest_filter():
    print("--- 启动全自动投研引擎 ---")
    print("正在通过 akshare 连接数据源...")
    
    # 1. 抓取A股最新实时行情
    df = ak.stock_zh_a_spot_em()
    
    # 2. 核心过滤逻辑：寻找具备护城河与安全边际的标的
    # 过滤掉亏损（PE<=0），筛选估值合理（PE<20）且总市值大于500亿（确定性高）的公司
    condition_pe = (df['市盈率-动态'] > 0) & (df['市盈率-动态'] < 20)
    condition_market_cap = df['总市值'] > 50000000000
    
    filtered_df = df[condition_pe & condition_market_cap].sort_values(by='市盈率-动态')
    
    print(f"\n✅ 成功筛选出符合【高壁垒+合理估值】逻辑的标的：{len(filtered_df)} 只")
    print("\n--- 核心观察池 (Top 10) ---")
    # 整理输出格式，方便你在 GitHub 日志里直接看
    result = filtered_df[['代码', '名称', '最新价', '市盈率-动态', '总市值']].head(10)
    print(result.to_string(index=False))

if __name__ == "__main__":
    value_invest_filter()
