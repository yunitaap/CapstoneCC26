import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

st.set_page_config(page_title="Dashboard EDA OLAH", layout="wide", page_icon="🍳")

# ── Dark/Light Mode Toggle ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan Tampilan")
    dark_mode = st.toggle("🌙 Dark Mode", value=False)

if dark_mode:
    BG        = "#1a1a2e"
    BG2       = "#16213e"
    CARD_BG   = "#0f3460"
    TEXT      = "#e0e0e0"
    TEXT_SUB  = "#aaaaaa"
    INSIGHT_BG = "#1e2a3a"
    INSIGHT_BORDER = "#FF6B35"
    DIVIDER   = "#333"
    FIG_BG    = "#1e1e2e"
    AX_BG     = "#1e1e2e"
    TICK_COLOR = "#aaaaaa"
    LABEL_COLOR = "#cccccc"
    ANNOT_COLOR = "#cccccc"
else:
    BG        = "#fafafa"
    BG2       = "#ffffff"
    CARD_BG   = "#ffffff"
    TEXT      = "#222222"
    TEXT_SUB  = "#555555"
    INSIGHT_BG = "#FFF8F0"
    INSIGHT_BORDER = "#FF6B35"
    DIVIDER   = "#eee"
    FIG_BG    = "#FAFAFA"
    AX_BG     = "#FAFAFA"
    TICK_COLOR = "#555555"
    LABEL_COLOR = "#555555"
    ANNOT_COLOR = "#444444"

# ── Inject CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    /* ── Global background ── */
    .stApp {{ background-color: {BG} !important; }}
    .main .block-container {{ background-color: {BG} !important; }}
    section[data-testid="stSidebar"] {{ background-color: {BG2} !important; }}

    /* ── Global text (non-card) ── */
    .stApp p, .stApp span, .stApp label,
    .stApp div, .stApp li, .stApp h1, .stApp h2, .stApp h3 {{
        color: {TEXT};
    }}

    /* ── Metric cards: flex center, white text immune to overrides ── */
    .metric-card, .metric-card2, .metric-card3, .metric-card4 {{
        border-radius: 16px;
        padding: 28px 20px;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 120px;
    }}
    .metric-card  {{ background: linear-gradient(135deg, #8a0f1c, #E71D36); box-shadow: 0 4px 14px rgba(231,29,54,0.4); }}
    .metric-card2 {{ background: linear-gradient(135deg, #a03500, #FF6B35); box-shadow: 0 4px 14px rgba(255,107,53,0.4); }}
    .metric-card3 {{ background: linear-gradient(135deg, #a06000, #FF9F1C); box-shadow: 0 4px 14px rgba(255,159,28,0.4); }}
    .metric-card4 {{ background: linear-gradient(135deg, #0a6e0d, #17DC20); box-shadow: 0 4px 14px rgba(23,220,32,0.4); }}

    .metric-card  .mc-num, .metric-card2 .mc-num,
    .metric-card3 .mc-num, .metric-card4 .mc-num {{
        font-size: 2.8rem; font-weight: 800; line-height: 1;
        color: #ffffff; margin-bottom: 8px;
    }}
    .metric-card  .mc-lbl, .metric-card2 .mc-lbl,
    .metric-card3 .mc-lbl, .metric-card4 .mc-lbl {{
        font-size: 0.92rem; color: rgba(255,255,255,0.88);
    }}

    /* ── Insight box ── */
    .insight-box {{
        background: {INSIGHT_BG};
        border-left: 5px solid {INSIGHT_BORDER};
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin-top: 10px;
        font-size: 0.92rem;
        color: {TEXT};
    }}
    .insight-box b {{ color: #FF6B35; }}

    /* ── Section title ── */
    .section-title {{
        font-size: 1.3rem; font-weight: 700;
        color: {TEXT}; margin-bottom: 4px;
    }}

    /* ── Top10 table ── */
    .top10-table {{ width: 100%; border-collapse: collapse; }}
    .top10-table th {{
        background: {'#0f3460' if dark_mode else '#FF6B35'};
        color: #ffffff; padding: 8px 12px;
        font-size: 0.88rem; text-align: left;
    }}
    .top10-table td {{
        padding: 7px 12px; font-size: 0.88rem;
        border-bottom: 1px solid {'#2a2a3e' if dark_mode else '#f0f0f0'};
        color: {TEXT};
        background: {BG2};
    }}
    .top10-table tr:hover td {{ background: {'#1e2a3a' if dark_mode else '#FFF3EB'}; }}
    .rank-badge {{
        display: inline-block; width: 26px; height: 26px;
        border-radius: 50%; text-align: center; line-height: 26px;
        font-weight: 800; font-size: 0.82rem; color: #ffffff;
    }}
    .loves-bar-wrap {{ background: {'#333' if dark_mode else '#ececec'}; border-radius: 4px; height: 10px; width: 100%; margin-bottom: 3px; }}
    .loves-bar-fill  {{ background: #FF6B35; border-radius: 4px; height: 10px; }}
    .loves-label {{ font-size: 0.82rem; color: {TEXT_SUB}; }}
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("streamlit/data_final.csv")
    return df

df = load_data()

COLORS = ["#E71D36","#FF6B35","#FF9F1C","#17DC20","#2EC4B6","#3A86FF","#8338EC","#7B2D8B"]
CAT_COLORS = {cat: COLORS[i % len(COLORS)] for i, cat in enumerate(df["Category"].unique())}

def make_fig(w=7, h=4.5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(FIG_BG)
    ax.set_facecolor(AX_BG)
    return fig, ax

def style_ax(ax, xlabel=None, ylabel=None):
    ax.spines[["top","right"]].set_visible(False)
    ax.spines["left"].set_color(TICK_COLOR)
    ax.spines["bottom"].set_color(TICK_COLOR)
    ax.tick_params(colors=TICK_COLOR, labelsize=9)
    if xlabel: ax.set_xlabel(xlabel, fontsize=10, color=LABEL_COLOR)
    if ylabel: ax.set_ylabel(ylabel, fontsize=10, color=LABEL_COLOR)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 🍳 DASHBOARD EDA OLAH")
st.markdown("### Punya bahan sisa makanan? Di-OLAH aja!")
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="mc-num">{df.shape[0]:,}</div><div class="mc-lbl">📋 Total Resep Tersedia</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card2"><div class="mc-num">{df["Category"].nunique()}</div><div class="mc-lbl">🗂️ Kategori Masakan</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card3"><div class="mc-num">{df["Loves"].sum():,}</div><div class="mc-lbl">❤️ Total Penyuka</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card4"><div class="mc-num">{df["Total Ingredients"].median():.0f}</div><div class="mc-lbl">🧂 Median Jumlah Bahan</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 1 — Top 10 Menu (tabel) + 3 Besar Kategori (pie + lainnya)
# ══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<p class="section-title">🏆 Top 10 Menu dengan Penyuka Terbanyak</p>', unsafe_allow_html=True)
    top10 = df.nlargest(10, "Loves")[["Title","Loves","Category"]].reset_index(drop=True)
    max_loves = top10["Loves"].max()

    medal = {0:"🥇", 1:"🥈", 2:"🥉"}
    rank_colors = ["#FFD700","#C0C0C0","#CD7F32"] + ["#FF6B35"]*7

    rows_html = ""
    for i, row in top10.iterrows():
        badge_color = rank_colors[i]
        rank_label  = medal.get(i, str(i+1))
        pct = row["Loves"] / max_loves * 100
        cat_color = CAT_COLORS.get(row["Category"], "#aaa")
        cat_badge = f'<span style="background:{cat_color};color:white;padding:2px 8px;border-radius:10px;font-size:0.78rem">{row["Category"]}</span>'
        bar_html  = f'<div class="loves-bar-wrap"><div class="loves-bar-fill" style="width:{pct:.0f}%"></div></div><div class="loves-label">❤️ {row["Loves"]:,}</div>'
        rows_html += f"""
        <tr>
          <td><span class="rank-badge" style="background:{badge_color}">{rank_label}</span></td>
          <td><b>{row['Title']}</b></td>
          <td>{cat_badge}</td>
          <td>{bar_html}</td>
        </tr>"""

    st.markdown(f"""
    <table class="top10-table">
      <thead><tr>
        <th>#</th><th>Nama Resep</th><th>Kategori</th><th>Penyuka</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>""", unsafe_allow_html=True)

    st.markdown("""<div class="insight-box">
        💡 <b>Insight:</b> <b>Bakso Sapi (Pakai Blender)</b> memimpin dengan <b>939 penyuka</b>, hampir 2 kali lipat resep kedua. 
        Artinya, resep <i>comfort food</i> klasik dengan metode yang dibuat lebih mudah sangat diminati.
        Kategori <b>sapi</b>, <b>ikan</b>, dan <b>tahu</b> mendominasi top 10, menandakan bahan-bahan terjangkau lebih populer.
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown('<p class="section-title">🥇 5 Besar Kategori + Lainnya</p>', unsafe_allow_html=True)

    cat_counts = df["Category"].value_counts()
    top5       = cat_counts.head(5)
    others_val = cat_counts.iloc[5:].sum()
    pie_labels = list(top5.index) + ["Lainnya"]
    pie_values = list(top5.values) + [others_val]
    pie_colors = [COLORS[0], COLORS[1], COLORS[2], COLORS[3], COLORS[4], "#999999"]

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor(FIG_BG)
    ax.set_facecolor(FIG_BG)
    wedges, texts, autotexts = ax.pie(
        pie_values,
        labels=pie_labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=pie_colors,
        explode=(0.05, 0.02, 0.02, 0.02, 0.02, 0.02),
        pctdistance=0.75,
        wedgeprops=dict(edgecolor=FIG_BG, linewidth=2)
    )
    for t in texts:
        t.set_fontsize(10); t.set_fontweight("bold"); t.set_color(TEXT)
    for at in autotexts:
        at.set_fontsize(9); at.set_color("white"); at.set_fontweight("bold")
    ax.set_title("dari seluruh resep", fontsize=10, color=TEXT_SUB, pad=6)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Lima kategori teratas meliputi <b>{top5.index[0]}</b> ({top5.values[0]:,}),
        <b>{top5.index[1]}</b> ({top5.values[1]:,}), <b>{top5.index[2]}</b> ({top5.values[2]:,}),
        <b>{top5.index[3]}</b> ({top5.values[3]:,}), dan <b>{top5.index[4]}</b> ({top5.values[4]:,}),
        mencakup <b>{top5.values[:5].sum()/len(df)*100:.1f}%</b> dari total keseluruhan resep.
        Jika dilihat, semuanya adalah bahan protein dan nabati dengan harga terjangkau yang menjadi andalan masakan rumahan Indonesia,
        sementara 3 kategori lain tergabung dalam <b>{others_val:,} resep</b> kategori lainnya.
    </div>""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 2 — Distribusi Bahan + Kategori vs Loves
# ══════════════════════════════════════════════════════════════════════════════
col3, col4 = st.columns(2)

with col3:
    st.markdown('<p class="section-title">🧂 Distribusi Jumlah Bahan per Resep</p>', unsafe_allow_html=True)
    fig, ax = make_fig()
    n, bins, patches_hist = ax.hist(df["Total Ingredients"].clip(upper=40), bins=35,
                                     edgecolor=FIG_BG, linewidth=0.6, alpha=0.9)
    for i, patch in enumerate(patches_hist):
        patch.set_facecolor(plt.cm.YlOrRd(i / len(patches_hist) * 0.8 + 0.1))
    median_val = df["Total Ingredients"].median()
    mean_val   = df["Total Ingredients"].mean()
    ax.axvline(median_val, color="#2EC4B6", linewidth=2, linestyle="--", label=f"Median: {median_val:.0f}")
    ax.axvline(mean_val,   color="#C77DFF", linewidth=2, linestyle=":",  label=f"Mean: {mean_val:.1f}")
    leg = ax.legend(fontsize=9, frameon=False)
    for t in leg.get_texts(): t.set_color(TEXT)
    style_ax(ax, "Jumlah Bahan", "Frekuensi Resep")
    plt.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Distribusi jumlah bahan condong ke kanan (<i>right-skewed</i>). Mayoritas resep menggunakan
        <b>8 hingga 15 bahan</b>, dengan median <b>{median_val:.0f} bahan</b>. Terdapat resep outlier dengan lebih dari 30 bahan,
        yang kemungkinan adalah resep kue atau masakan tradisional kompleks.
        Ini mengindikasikan bahwa sebagian besar dataset berisi resep sederhana.
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown('<p class="section-title">❤️ Rata-rata Penyuka per Kategori</p>', unsafe_allow_html=True)
    cat_loves = df.groupby("Category")["Loves"].agg(["mean","median"]).reset_index()
    cat_loves = cat_loves.sort_values("mean", ascending=False)
    bar_colors = [CAT_COLORS.get(c, "#aaa") for c in cat_loves["Category"]]

    fig, ax = make_fig()
    x = np.arange(len(cat_loves))
    b1 = ax.bar(x - 0.2, cat_loves["mean"],   0.35, label="Rata-rata", color=bar_colors, alpha=0.9, edgecolor=FIG_BG)
    b2 = ax.bar(x + 0.2, cat_loves["median"], 0.35, label="Median",    color=bar_colors, alpha=0.45, edgecolor=FIG_BG)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_loves["Category"], rotation=30, ha="right", fontsize=9.5, color=TICK_COLOR)
    for bar in b1:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=7.5, color=ANNOT_COLOR)
    leg = ax.legend(fontsize=9, frameon=False)
    for t in leg.get_texts(): t.set_color(TEXT)
    style_ax(ax, ylabel="Jumlah Penyuka")
    plt.tight_layout(); st.pyplot(fig); plt.close()

    top_avg_cat = cat_loves.iloc[0]["Category"]
    top_avg_val = cat_loves.iloc[0]["mean"]
    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Kategori <b>{top_avg_cat}</b> memiliki rata-rata penyuka tertinggi ({top_avg_val:.1f}).
        Selisih besar antara <i>mean</i> dan <i>median</i> di semua kategori menunjukkan distribusi yang sangat <i>condong</i>,
        karena ada beberapa resep viral yang menaikkan rata-rata.
        Artinya, mayoritas resep masih memiliki penyuka di bawah rata-rata.
    </div>""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 3 — Jumlah Resep per Kategori + Distribusi Langkah
# ══════════════════════════════════════════════════════════════════════════════
col5, col6 = st.columns(2)

with col5:
    st.markdown('<p class="section-title">🗂️ Jumlah Resep per Kategori</p>', unsafe_allow_html=True)
    cat_count = df["Category"].value_counts().reset_index()
    cat_count.columns = ["Category", "Count"]
    bar_colors2 = [CAT_COLORS.get(c, "#aaa") for c in cat_count["Category"]]

    fig, ax = make_fig()
    bars = ax.bar(cat_count["Category"], cat_count["Count"],
                  color=bar_colors2, edgecolor=FIG_BG, linewidth=0.8)
    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10,
                f"{int(bar.get_height()):,}", ha="center", va="bottom",
                fontsize=9, fontweight="bold", color=ANNOT_COLOR)
    style_ax(ax, "Kategori", "Jumlah Resep")
    ax.tick_params(axis="x", rotation=25)
    plt.tight_layout(); st.pyplot(fig); plt.close()

    most  = cat_count.iloc[0]
    least = cat_count.iloc[-1]
    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Dataset cukup <b>seimbang</b> antar kategori, dengan rentang antara kategori terbanyak
        (<b>{most['Category']}</b>: {most['Count']:,}) dan tersedikit (<b>{least['Category']}</b>: {least['Count']:,})
        hanya sekitar {(most['Count']-least['Count']):,} resep. Ini menandakan dataset sudah representatif,
        cocok untuk pelatihan model rekomendasi yang tidak bias kategori.
    </div>""", unsafe_allow_html=True)

with col6:
    st.markdown('<p class="section-title">👨‍🍳 Distribusi Jumlah Langkah Memasak</p>', unsafe_allow_html=True)
    fig, ax = make_fig()
    n2, bins2, patches2 = ax.hist(df["Total Steps"].clip(upper=30), bins=28,
                                   edgecolor=FIG_BG, linewidth=0.6, alpha=0.9)
    for i, patch in enumerate(patches2):
        patch.set_facecolor(plt.cm.cool(i / len(patches2) * 0.8 + 0.1))
    med_s  = df["Total Steps"].median()
    mean_s = df["Total Steps"].mean()
    ax.axvline(med_s,  color=COLORS[0], linewidth=2, linestyle="--", label=f"Median: {med_s:.0f}")
    ax.axvline(mean_s, color=COLORS[3], linewidth=2, linestyle=":",  label=f"Mean: {mean_s:.1f}")
    leg = ax.legend(fontsize=9, frameon=False)
    for t in leg.get_texts(): t.set_color(TEXT)
    style_ax(ax, "Jumlah Langkah", "Frekuensi Resep")
    plt.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Mayoritas resep memiliki sekitar <b>{med_s:.0f} hingga {mean_s:.0f} langkah</b> memasak.
        Distribusi yang terpusat ini mengindikasikan sebagian besar pengguna menulis resep dengan tingkat detail yang serupa.
        Resep dengan lebih dari 20 langkah kemungkinan adalah resep yang kompleks.
    </div>""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 4 — Scatter Bahan vs Loves + Segmentasi Popularitas
# ══════════════════════════════════════════════════════════════════════════════
col7, col8 = st.columns(2)

with col7:
    st.markdown('<p class="section-title">📊 Jumlah Bahan vs Penyuka</p>', unsafe_allow_html=True)
    sample = df[df["Loves"] <= 200].sample(min(2000, len(df)), random_state=42)
    scatter_colors = [CAT_COLORS.get(c, "#aaa") for c in sample["Category"]]

    fig, ax = make_fig()
    ax.scatter(sample["Total Ingredients"], sample["Loves"],
               c=scatter_colors, alpha=0.35, s=18, edgecolors="none")
    z  = np.polyfit(sample["Total Ingredients"], sample["Loves"], 1)
    xs = np.linspace(sample["Total Ingredients"].min(), sample["Total Ingredients"].max(), 100)
    ax.plot(xs, np.poly1d(z)(xs), color="#E71D36", linewidth=2, linestyle="--")
    patches_sc = [mpatches.Patch(color=v, label=k) for k, v in CAT_COLORS.items()]
    leg = ax.legend(handles=patches_sc, fontsize=7.5, frameon=False, loc="upper right", ncol=2)
    for t in leg.get_texts(): t.set_color(TEXT)
    style_ax(ax, "Jumlah Bahan", "Jumlah Penyuka")
    plt.tight_layout(); st.pyplot(fig); plt.close()

    corr = df["Total Ingredients"].corr(df["Loves"])
    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Korelasi antara jumlah bahan dan penyuka sangat lemah (<b>r = {corr:.2f}</b>).
        Artinya, <b>banyaknya bahan bukan penentu popularitas</b> sebuah resep.
        Resep simpel pun bisa viral jika metodenya menarik atau hasilnya ikonik.
    </div>""", unsafe_allow_html=True)

with col8:
    st.markdown('<p class="section-title">💬 Segmentasi Popularitas Resep</p>', unsafe_allow_html=True)
    bins_loves   = [-1, 0, 5, 20, 50, 200, df["Loves"].max()+1]
    labels_loves = ["0 Suka", "1-5", "6-20", "21-50", "51-200", "200+"]
    df["Popularity"] = pd.cut(df["Loves"], bins=bins_loves, labels=labels_loves)
    pop_counts = df["Popularity"].value_counts().reindex(labels_loves)

    fig, ax = make_fig()
    bar_pop = ax.bar(pop_counts.index, pop_counts.values,
                     color=COLORS[:len(labels_loves)], edgecolor=FIG_BG)
    for bar in bar_pop:
        pct = bar.get_height() / len(df) * 100
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+30,
                f"{pct:.1f}%", ha="center", va="bottom",
                fontsize=9.5, fontweight="bold", color=ANNOT_COLOR)
    style_ax(ax, "Segmen Popularitas", "Jumlah Resep")
    plt.tight_layout(); st.pyplot(fig); plt.close()

    niche_pct = (pop_counts["0 Suka"] + pop_counts["1-5"]) / len(df) * 100
    viral_pct  = pop_counts["200+"] / len(df) * 100
    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Sebanyak <b>{niche_pct:.1f}%</b> resep memiliki 0 hingga 5 penyuka,
        menunjukkan adanya <i>long-tail distribution</i>.
        Hanya <b>{viral_pct:.1f}%</b> resep yang menembus 200 penyuka (viral).
        Ini peluang besar bagi sistem rekomendasi untuk membantu resep berkualitas
        yang belum terdiscovery agar mendapat eksposur lebih luas.
    </div>""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 5 — Scatter Bahan vs Steps + Eksplorasi interaktif
# ══════════════════════════════════════════════════════════════════════════════
col9, col10 = st.columns(2)

with col9:
    st.markdown('<p class="section-title">🔗 Jumlah Bahan vs Jumlah Langkah</p>', unsafe_allow_html=True)
    samp2 = df.sample(min(3000, len(df)), random_state=7)
    sc_colors2 = [CAT_COLORS.get(c, "#aaa") for c in samp2["Category"]]

    fig, ax = make_fig()
    ax.scatter(samp2["Total Ingredients"], samp2["Total Steps"],
               c=sc_colors2, alpha=0.3, s=14, edgecolors="none")
    z2  = np.polyfit(samp2["Total Ingredients"], samp2["Total Steps"], 1)
    xs2 = np.linspace(samp2["Total Ingredients"].min(), samp2["Total Ingredients"].max(), 100)
    ax.plot(xs2, np.poly1d(z2)(xs2), color="#E71D36", linewidth=2, linestyle="--")
    patches4 = [mpatches.Patch(color=v, label=k) for k, v in CAT_COLORS.items()]
    leg = ax.legend(handles=patches4, fontsize=7.5, frameon=False, ncol=2, loc="upper left")
    for t in leg.get_texts(): t.set_color(TEXT)
    style_ax(ax, "Jumlah Bahan", "Jumlah Langkah")
    plt.tight_layout(); st.pyplot(fig); plt.close()

    corr2 = df["Total Ingredients"].corr(df["Total Steps"])
    st.markdown(f"""<div class="insight-box">
        💡 <b>Insight:</b> Ada korelasi positif moderat (<b>r = {corr2:.2f}</b>) antara jumlah bahan dan langkah,
        yang berarti semakin banyak bahan, semakin panjang prosesnya. Namun banyak <i>outlier</i>,
        seperti resep dengan bahan sedikit tapi langkah banyak (teknik mendetail),
        dan sebaliknya pada memasak <i>one-pot</i>.
    </div>""", unsafe_allow_html=True)

with col10:
    st.markdown('<p class="section-title">🔍 Eksplorasi Top Resep per Kategori</p>', unsafe_allow_html=True)
    selected_cat = st.selectbox("Pilih Kategori:", sorted(df["Category"].unique()))
    top_n = st.slider("Tampilkan Top N:", 0, 15, 3)

    cat_df = df[df["Category"] == selected_cat].nlargest(top_n, "Loves")[
        ["Title","Loves","Total Ingredients","Total Steps"]].reset_index(drop=True)
    cat_df.index += 1

    fig, ax = plt.subplots(figsize=(7, max(3, top_n * 0.55)))
    fig.patch.set_facecolor(FIG_BG); ax.set_facecolor(AX_BG)
    sel_color = CAT_COLORS.get(selected_cat, COLORS[0])
    ax.barh(cat_df["Title"][::-1], cat_df["Loves"][::-1],
            color=sel_color, edgecolor=FIG_BG, height=0.6, alpha=0.88)
    for i, (_, row) in enumerate(cat_df[::-1].iterrows()):
        ax.text(row["Loves"] + 2, i,
                f"♥{row['Loves']}  bhn:{row['Total Ingredients']}  step:{row['Total Steps']}",
                va="center", fontsize=8.5, color=ANNOT_COLOR)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.spines["bottom"].set_color(TICK_COLOR)
    ax.tick_params(colors=TICK_COLOR, labelsize=9)
    ax.set_xlabel("Jumlah Penyuka", fontsize=10, color=LABEL_COLOR)
    plt.tight_layout(); st.pyplot(fig); plt.close()

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 6 — Word Cloud Bahan
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-title">☁️ Bahan yang Paling Sering Digunakan</p>', unsafe_allow_html=True)
 
wc_col1, wc_col2 = st.columns([2, 1])
 
wc_cats = ["Semua Kategori"] + sorted(df["Category"].unique().tolist())
selected_wc_cat = st.selectbox("Filter kategori:", wc_cats, key="wc_cat")
 
# Stopwords bahan umum yang kurang informatif
STOPWORDS_BAHAN = {
    "air", "minyak", "garam", "gula", "secukupnya", "sdm", "sdt",
    "liter", "ml", "gr", "kg", "gram", "buah", "siung", "lembar",
    "batang", "iris", "potong", "halus", "goreng", "iris", "minyakk"

    }
with wc_col1:
    try:
        from wordcloud import WordCloud
 
        if selected_wc_cat == "Semua Kategori":
            wc_df = df
        else:
            wc_df = df[df["Category"] == selected_wc_cat]
 
        # Gabung semua teks bahan
        all_ingredients = " ".join(wc_df["Ingredients Final"].dropna().astype(str).tolist())
 
        wc = WordCloud(
            width=800, height=400,
            background_color=FIG_BG,
            colormap="Set1" if not dark_mode else "cool",
            stopwords=STOPWORDS_BAHAN,
            max_words=80,
            prefer_horizontal=0.85,
            collocations=False,
            min_font_size=10,
        ).generate(all_ingredients)
 
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor(FIG_BG)
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(fig)
        plt.close()
 
    except ImportError:
        st.warning("Library `wordcloud` belum terinstall. Jalankan: `pip install wordcloud`")
 
with wc_col2:
    st.markdown("<br>", unsafe_allow_html=True)
 
    # Top 15 bahan terbanyak sebagai tabel pendamping
    from collections import Counter
    import re
 
    if selected_wc_cat == "Semua Kategori":
        count_df = df
    else:
        count_df = df[df["Category"] == selected_wc_cat]
 
    all_words = " ".join(count_df["Ingredients Final"].dropna().astype(str)).split()
    filtered  = [w for w in all_words if w not in STOPWORDS_BAHAN and len(w) > 2]
    top_bahan = Counter(filtered).most_common(15)
 
    bahan_df = pd.DataFrame(top_bahan, columns=["Bahan", "Frekuensi"])
    max_freq  = bahan_df["Frekuensi"].max()
 
    rows = ""
    for i, row in bahan_df.iterrows():
        pct  = row["Frekuensi"] / max_freq * 100
        color = COLORS[i % len(COLORS)]
        rows += f"""<tr>
            <td style="padding:5px 8px;color:{TEXT};font-size:0.88rem">{i+1}. {row['Bahan']}</td>
            <td style="padding:5px 8px;width:55%">
                <div style="background:{'#333' if dark_mode else '#eee'};border-radius:4px;height:8px">
                    <div style="background:{color};width:{pct:.0f}%;height:8px;border-radius:4px"></div>
                </div>
                <span style="font-size:0.78rem;color:{TEXT_SUB}">{row['Frekuensi']:,}x</span>
            </td>
        </tr>"""
 
    st.markdown(f"""
    <table style="width:100%;border-collapse:collapse">
      <thead><tr>
        <th style="background:{'#0f3460' if dark_mode else '#E71D36'};color:white;padding:8px;font-size:0.85rem;text-align:left;border-radius:8px 0 0 0">Bahan</th>
        <th style="background:{'#0f3460' if dark_mode else '#E71D36'};color:white;padding:8px;font-size:0.85rem;text-align:left;border-radius:0 8px 0 0">Frekuensi</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)
 
st.markdown(f"""<div class="insight-box">
    💡 <b>Insight:</b> Bahan yang paling dominan adalah bumbu dasar masakan Indonesia seperti
    <b>bawang merah</b>, <b>bawang putih</b>, <b>cabai</b>, dan <b>kemiri</b>.
    Dominasi bumbu dasar ini menunjukkan bahwa mayoritas resep dalam dataset adalah masakan Indonesia otentik
    yang mengandalkan rempah lokal sebagai fondasi rasa,
    bukan masakan fusion atau western yang umumnya menggunakan bumbu berbeda.
</div>""", unsafe_allow_html=True)
 
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("📋 Lihat Preview Dataset & Info"):
    c_a, c_b = st.columns(2)
    with c_a:
        st.write("**5 Baris Pertama**")
        st.dataframe(df[["Title","Category","Loves","Total Ingredients","Total Steps"]].head(), use_container_width=True)
    with c_b:
        st.write("**Missing Values**")
        mv = df.isna().sum().reset_index()
        mv.columns = ["Kolom", "Null"]
        st.dataframe(
            mv[mv["Null"] > 0] if mv["Null"].sum() > 0
            else pd.DataFrame({"Info": ["Tidak ada missing values."]}),
            use_container_width=True
        )

st.markdown(f"<br><center style='color:{TEXT_SUB};font-size:0.85rem'>Dashboard EDA OLAH · Capstone Project · CC26-PSU127</center>", unsafe_allow_html=True)