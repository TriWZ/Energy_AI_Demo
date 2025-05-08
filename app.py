
import streamlit as st
import numpy_financial as npf
import matplotlib.pyplot as plt
import openai

# --- 页面标题 ---
st.title("Triphorium AI 节能优化分析助手")

# --- 用户输入 ---
investment = st.number_input("投资总额（USD）", value=30000)
annual_saving_kwh = st.number_input("年节省电量（kWh）", value=18000)
electricity_price = st.number_input("电价（USD/kWh）", value=0.18)
lifespan_years = st.slider("预计使用年限", 1, 20, 10)

# --- 回报计算 ---
annual_saving_usd = annual_saving_kwh * electricity_price
roi = annual_saving_usd / investment
payback = investment / annual_saving_usd
irr = npf.irr([-investment] + [annual_saving_usd]*lifespan_years)

st.markdown("### 财务分析结果")
st.write(f"- 年节省金额：${annual_saving_usd:,.2f}")
st.write(f"- ROI：{roi:.2%}")
st.write(f"- 回收周期：{payback:.2f} 年")
st.write(f"- IRR：{irr:.2%}")

# --- 图表展示 ---
years = list(range(1, lifespan_years + 1))
cashflow = [annual_saving_usd * i for i in years]

fig, ax = plt.subplots()
ax.plot(years, cashflow, label="累计节省")
ax.axhline(investment, color='red', linestyle='--', label="投资额")
ax.set_xlabel("年数")
ax.set_ylabel("USD")
ax.set_title("累计节能 vs 投资成本")
ax.legend()
st.pyplot(fig)

# --- OpenAI 建议 ---
st.markdown("### AI 分析建议")

openai.api_key = st.text_input("请输入你的 OpenAI API Key", type="password")

if openai.api_key:
    prompt = f"""
    假设我对一栋建筑进行了${investment}美元的节能改造，预计每年节省{annual_saving_kwh}度电，
    电价为{electricity_price}美元/度，总回收周期为{payback:.2f}年，请用专业口吻给出：
    1. 此项目的节能意义；
    2. 如何进一步优化；
    3. 建议我是否在其他项目中复制此方案。
    """
    with st.spinner("AI 正在生成分析，请稍等..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(response['choices'][0]['message']['content'])
