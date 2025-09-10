import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 최종 데미지 계산 함수
def compute_z(buff_x, buff_y, atk, E_def, def_coef, Weak_coef, sk_coef):
    numer = atk ** 2
    denomi = atk + E_def * (1 - def_coef * 0.01)
    return (numer / denomi) * (1 + buff_x * 0.01) * (1+Weak_coef*0.1) * (sk_coef * 0.01) * (buff_y * 0.01)

st.title("무기 효율 계산기 (데미지 + 효율 그래프)")

# 공통 변수
st.sidebar.header("공통 변수 설정")
E_def = st.sidebar.number_input("적 방어력", min_value=0.0, value=5000.0, max_value=20000.0, step=100.0, format="%.0f")
atk_origin = st.sidebar.number_input("기초 공격력", min_value=2000.0, max_value=5000.0, value=3500.0, step=10.0, format="%.0f")
def_coef = st.sidebar.number_input("방어 무시(%)", min_value=0.0, max_value=100.0, value=30.0, step=10.0, format="%.0f")
Weak_coef = st.sidebar.number_input("약점 (개)", min_value=0.0, max_value=2.0, value=0.0, step=1.0, format="%.0f")
sk_coef = st.sidebar.number_input("스킬 계수(%)", min_value=0.0, max_value=1500.0, value=100.0, step=10.0, format="%.0f")
buff_x = st.sidebar.number_input("피해 증가(%)", min_value=0.0, max_value=800.0, value=0.0, step=10.0, format="%.0f")
buff_y = st.sidebar.number_input("치명 피해(%)", min_value=0.0, max_value=500.0, value=120.0, step=10.0, format="%.0f")


# 무기 A
st.subheader("무기 A")

wepA_ak = 0
wepA_ct = 0
choice_A = st.radio(
    "무기 옵션",
    options=["공격 보너스 15%", "치명타 피해 25%"],
    horizontal=True,
    key="weaponA_option"
)
if choice_A == "공격 보너스 15%":
    wepA_ak = 15
elif choice_A == "치명타 피해 25%":
    wepA_ct = 25

def_A = st.number_input("방어 무시(%)", min_value=0.0, max_value=20.0, value=0.0, step=10.0, format="%.0f", key="def_ignore_A")
total_def_A = min(def_A + def_coef, 100)

col1, col2 = st.columns([2, 1])
with col1:
    dmg_A_slider = st.slider("피증 계수 (합산)", 0.0, 600.0, 10.0, step=10.0, format="%.0f", key="dmg_buff_A")
with col2:
    dmg_A_input = st.number_input("직접 입력 (적용 값)", min_value=0.0, max_value=600.0, value=dmg_A_slider, step=10.0, format="%.0f", key="dmg_buff_A_w")
    
dmg_A = dmg_A_input



# 무기 B
st.subheader("무기 B")

wepB_ak = 0
wepB_ct = 0
choice_B = st.radio(
    "무기 옵션",
    options=["공격 보너스 15%", "치명타 피해 25%"],
    horizontal=True,
    key="weaponB_option"
)
if choice_B == "공격 보너스 15%":
    wepB_ak = 15
elif choice_B == "치명타 피해 25%":
    wepB_ct = 25

def_B = st.number_input("방어 무시(%)", min_value=0.0, max_value=20.0, value=0.0, step=10.0, format="%.0f", key="def_ignore_B")
total_def_B = min(def_B + def_coef, 100)

col1, col2 = st.columns([2, 1])
with col1:
    dmg_B_slider = st.slider("피증 계수 (합산)", 0.0, 600.0, 10.0, step=10.0, format="%.0f", key="dmg_buff_B")
with col2:
    dmg_B_input = st.number_input("직접 입력 (적용 값)", min_value=0.0, max_value=600.0, value=dmg_B_slider, step=10.0, format="%.0f", key="dmg_buff_B_w")
    
dmg_B = dmg_B_input

# 결과 계산
damage_A = compute_z(buff_x + dmg_A, buff_y + wepB_ct, atk_A, E_def, total_def_A, Weak_coef, sk_A)
damage_B = compute_z(buff_x + dmg_B, buff_y + wepB_ct, atk_B, E_def, total_def_B, Weak_coef, sk_B)

diff = damage_B - damage_A
efficiency = (damage_B / damage_A - 1) * 100 if damage_A != 0 else 0

st.markdown("### 결과")
st.write(f"무기 A 최종 데미지: **{damage_A:,.2f}**")
st.write(f"무기 B 최종 데미지: **{damage_B:,.2f}**")

if diff > 0:
    st.success(f"무기 B가 {diff:,.2f} 만큼 강력하며, 효율은 {efficiency:.2f}% 더 좋습니다.")
elif diff < 0:
    st.error(f"무기 A가 {-diff:,.2f} 만큼 강력하며, 효율은 {-efficiency:.2f}% 더 좋습니다.")
else:
    st.info("무기 A와 B의 최종 데미지가 동일합니다.")

# 📈 그래프: 데미지 곡선 + 효율(%) 곡선
atk_range = np.linspace(100, 5000, 200)
damage_curve_A = [compute_z(buff_x, buff_y, atk, E_def, def_coef, Weak_coef, sk_A) for atk in atk_range]
damage_curve_B = [compute_z(buff_x, buff_y, atk, E_def, def_coef, Weak_coef, sk_B) for atk in atk_range]
efficiency_curve = [(b/a - 1) * 100 if a != 0 else 0 for a, b in zip(damage_curve_A, damage_curve_B)]

fig, ax1 = plt.subplots(figsize=(9,6))

# 데미지 곡선 (왼쪽 y축)
ax1.plot(atk_range, damage_curve_A, label="무기 A 데미지", color="blue")
ax1.plot(atk_range, damage_curve_B, label="무기 B 데미지", color="red")
ax1.set_xlabel("공격력 (ATK)")
ax1.set_ylabel("최종 데미지")
ax1.legend(loc="upper left")
ax1.grid(True)

# 효율 곡선 (오른쪽 y축)
ax2 = ax1.twinx()
ax2.plot(atk_range, efficiency_curve, label="효율 (B vs A, %)", color="green", linestyle="--")
ax2.set_ylabel("효율 (%)")
ax2.axhline(0, color="black", linestyle=":")
ax2.legend(loc="upper right")

st.pyplot(fig)
