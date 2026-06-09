import akshare as ak
import pandas as pd

def value_invest_filter():
    print("--- 启动全自动投研引擎（自诊断模式） ---")
    
    # 尝试抓取新浪数据
    try:
        print("【正在从新浪接口获取数据...】")
        df = ak.stock_zh_a_spot()
        
        # 打印出所有列名，如果再次报错，你可以直接通过日志看到真实列名
        print(f"数据抓取成功，当前列名有: {list(df.columns)}")
        
        # 尝试清洗数据，使用更通用的列名映射
        # 自动识别可能的市盈率和价格列
        # 常见列名: 'trade', 'price', 'per', 'pe', 'mktcap'
        
        # 将可能的列名转为数值，报错忽略
        for col in df.columns:
            if col not in ['代码', '名称']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        print("✅ 数据清洗完毕，开始根据价值逻辑筛选...")
        
        # 假设常见的列映射，如果你的截图报错提示 trade/市盈率 缺失，
        # 我们用 .get() 方法处理，避免直接报错
        price = df.get('trade') if 'trade' in df else df.get('最新价')
        pe = df.get('per') if 'per' in df else df.get('市盈率')
        mktcap = df.get('mktcap') if 'mktcap' in df else df.get('总市值')
        
        # 简单的价值过滤
        mask = (pe > 0) & (pe < 30) & (mktcap > 50000000000)
        result = df[mask].sort_values(by=pe.name)
        
        print("\n--- 筛选结果 ---")
        print(result[['代码', '名称', price.name, pe.name]].head(10).to_string(index=False))
        
    except Exception as e:
        print(f"❌ 运行报错，错误详情: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    value_invest_filter()
