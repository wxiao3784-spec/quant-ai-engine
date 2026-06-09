import akshare as ak
import pandas as pd
import time

def value_invest_filter():
    print("--- 启动全自动投研引擎 ---")
    df = None
    
    # 【方案A】优先尝试新浪数据源（新浪对海外IP的容忍度通常显著高于东财）
    print("【正在尝试新浪核心数据源...】")
    try:
        df = ak.stock_zh_a_spot()
        if df is not None and not df.empty:
            print("✅ 新浪数据抓取成功！正在清洗数据...")
            # 统一字段名以匹配价值投资逻辑
            df = df.rename(columns={
                'trade': '最新价', 
                'per': '市盈率-动态', 
                'mktcap': '总市值'
            })
            df['市盈率-动态'] = pd.to_numeric(df['市盈率-动态'], errors='coerce')
            # 新浪总市值单位是万元，换算成元
            df['总市值'] = pd.to_numeric(df['总市值'], errors='coerce') * 10000
            df['最新价'] = pd.to_numeric(df['最新价'], errors='coerce')
    except Exception as e:
        print(f"⚠️ 新浪数据源被拦截: {e}")

    # 【方案B】如果新浪失败，带上延迟重试，再战东财数据源
    if df is None or df.empty:
        print("【新浪通道受阻，正在启用东财备用通道并尝试抗封锁重试...】")
        for i in range(3):
            try:
                time.sleep(2)  # 每次重试前歇2秒，降低被封几率
                df = ak.stock_zh_a_spot_em()
                if df is not None and not df.empty:
                    print(f"✅ 第 {i+1}次重试成功突破东财防火墙！")
                    break
            except Exception as e:
                print(f"❌ 第 {i+1} 次东财尝试失败...")

    # 如果都失败了，安全退出
    if df is None or df.empty:
        print("❌ 核心财经数据源均被海外IP暂时拦截，请稍后再试或更换代理。")
        return

    # 核心过滤逻辑：寻找具备深厚护城河（大市值）+ 安全边际（低估值）的标的
    try:
        # 过滤掉亏损公司，筛选动态市盈率在 0 到 20 之间的合理估值标的
        condition_pe = (df['市盈率-动态'] > 0) & (df['市盈率-动态'] < 20)
        # 筛选总市值大于 500 亿人民币（高确定性的大底盘公司）
        condition_market_cap = df['总市值'] > 50000000000
        
        filtered_df = df[condition_pe & condition_market_cap].sort_values(by='市盈率-动态')
        
        print(f"\n✅ 成功筛选出符合【高壁垒 + 合理估值】长期主义逻辑的标的：{len(filtered_df)} 只")
        print("\n--- 核心观察池 (Top 10) ---")
        
        # 提取核心展示字段
        result = filtered_df[['代码', '名称', '最新价', '市盈率-动态', '总市值']].head(10)
        # 格式化市值显示，更具可读性
        result['总市值'] = (result['总市值'] / 100000000).round(2).astype(str) + ' 亿'
        print(result.to_string(index=False))
        
    except Exception as e:
        print(f"❌ 数据筛选过滤时出现预期外错误: {e}")

if __name__ == "__main__":
    value_invest_filter()
