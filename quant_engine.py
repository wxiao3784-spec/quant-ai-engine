import akshare as ak
import pandas as pd
import time

def value_invest_filter():
    print("--- 启动全自动投研引擎 ---")
    df = None
    
    print("【正在尝试新浪核心数据源...】")
    try:
        df = ak.stock_zh_a_spot()
        if df is not None and not df.empty:
            print("✅ 新浪数据抓取成功！开始对齐字段...")
            
            # 强制转换数据类型，防止文本导致计算报错
            df['trade'] = pd.to_numeric(df['trade'], errors='coerce')  # 最新价
            df['per'] = pd.to_numeric(df['per'], errors='coerce')      # 市盈率
            df['mktcap'] = pd.to_numeric(df['mktcap'], errors='coerce')  # 总市值（万元）
            
            # 新浪的总市值单位是万元，我们换算成“亿元”方便看
            df['总市值(亿)'] = (df['mktcap'] / 10000).round(2)
            
            # 统一改名，方便后续过滤
            df = df.rename(columns={
                'code': '代码',
                'name': '名称',
                'trade': '最新价', 
                'per': '市盈率'
            })
    except Exception as e:
        print(f"⚠️ 新浪数据源读取失败: {e}")

    if df is None or df.empty:
        print("❌ 未获取到任何数据，请检查接口。")
        return

    # 执行价值投资过滤逻辑
    try:
        # 1. 过滤掉亏损和高估值公司（市盈率在 0 到 20 之间）
        condition_pe = (df['市盈率'] > 0) & (df['市盈率'] < 20)
        
        # 2. 筛选总市值大于 500 亿人民币（也就是 500 亿）的公司
        condition_market_cap = df['总市值(亿)'] > 500
        
        filtered_df = df[condition_pe & condition_market_cap].sort_values(by='市盈率')
        
        print(f"\n✅ 成功筛选出符合【大市值 + 低估值】逻辑的标的：{len(filtered_df)} 只")
        print("\n--- 核心观察池 (Top 10) ---")
        
        # 提取并展示核心数据
        result = filtered_df[['代码', '名称', '最新价', '市盈率', '总市值(亿)']].head(10)
        # 给总市值加上“亿”字后缀方便阅读
        result['总市值(亿)'] = result['总市值(亿)'].astype(str) + ' 亿'
        
        print(result.to_string(index=False))
        
    except Exception as e:
        print(f"❌ 数据筛选过滤时出现预期外错误: {e}")

if __name__ == "__main__":
    value_invest_filter()
