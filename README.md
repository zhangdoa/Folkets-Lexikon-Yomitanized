# 📚 Folkets Lexikon for Yomitan

[![Build Dictionary](https://github.com/zhangdoa/Folkets-Lexikon-Yomitanized/actions/workflows/build-dictionary.yml/badge.svg)](https://github.com/zhangdoa/Folkets-Lexikon-Yomitanized/actions/workflows/build-dictionary.yml)

A comprehensive Yomitan dictionary built from the authoritative [Folkets Lexikon](https://folkets-lexikon.csc.kth.se/folkets/om.en.html) Swedish-English database maintained by KTH Royal Institute of Technology.

## 🚀 Quick Download

1. Navigate to [**Actions**](../../actions/workflows/build-dictionary.yml)
2. Click **"Run workflow"** → **"Run workflow"** (green button)
3. Wait 2-3 minutes for build completion
4. Download the generated artifact ZIP file
5. **Extract** the artifact to get the actual dictionary file: `folkets-lexikon-yomitan-v*.zip`

## 📱 Installation in Yomitan

1. **Download** the dictionary ZIP file from Actions
2. **Extract** the downloaded artifact to get the actual dictionary file
3. **Open** Yomitan extension settings (click the extension icon → settings gear)
4. **Navigate** to **"Dictionaries"** in the left sidebar
5. **Click** **"Import"** button
6. **Select** the **extracted** dictionary ZIP file (not the artifact ZIP)
7. **Enable** the dictionary by toggling it on
8. **Enjoy** instant Swedish translations!

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Comprehensive** | 30,000+ Swedish-English entries |
| 🔄 **Always Fresh** | Built on-demand from latest Folkets Lexikon data |
| 📝 **Rich Content** | Usage examples, translations, and context |
| 🔤 **Word Forms** | Complete inflection and conjugation information |
| 🎯 **Structured** | Semantic markup for better readability |
| ⚡ **Fast Import** | Optimized dictionary format for quick loading |

## 🔧 Build Locally

Requirements: Python 3.7+

```bash
# Clone the repository
git clone https://github.com/zhangdoa/Folkets-Lexikon-Yomitanized.git
cd Folkets-Lexikon-Yomitanized

# Download source data (automatically fetched, or manual download)
curl -o folkets_sv_en_public.xml https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xml

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Build the dictionary
python __main__.py
```

The generated `Folkets_Lexikon.zip` file can be imported directly into Yomitan.

## 🛠️ Technical Details

- **Format**: Yomitan v3 dictionary format
- **Source**: Folkets Lexikon XML database
- **Processing**: Structured content with semantic markup
- **Compression**: ZIP with optimal compression
- **Encoding**: UTF-8 throughout

## 🤝 Contributing

We welcome contributions! Whether it's:
- 🐛 Bug reports
- 💡 Feature requests  
- 📖 Documentation improvements
- 🔧 Code contributions

Please check our [Issues](../../issues) or create a new one.

## 🤖 Development Note

This project was collaboratively developed through human-AI cooperation with **Claude (Anthropic)**:
- **Human guidance**: Requirements definition, feedback, quality control, and project direction by [@zhangdoa](https://github.com/zhangdoa)
- **AI implementation**: Code development, documentation writing, and technical solutions by Claude Sonnet 4
- **Iterative refinement**: Continuous feedback loop between human and AI to achieve the final result

This represents a practical example of human-AI collaboration in software development, where Claude serves as a coding partner while the human provides vision, judgment, and oversight. The entire codebase was generated through conversational programming with Claude.

## 📄 License

This project and the generated dictionary are licensed under **Creative Commons Attribution-ShareAlike 2.5 Generic** to maintain compatibility with the original Folkets Lexikon data.

### Attribution
- **Original Data**: [Folkets Lexikon](https://folkets-lexikon.csc.kth.se/) by KTH Royal Institute of Technology
- **License**: [CC BY-SA 2.5 Generic](https://creativecommons.org/licenses/by-sa/2.5/)
- **Conversion**: This community project

### Usage Rights
✅ **Use** - Free for personal and commercial use  
✅ **Modify** - You can adapt and build upon the material  
✅ **Share** - You can distribute the material  
⚠️ **Share Alike** - If you remix or build upon the material, you must distribute under the same license  
⚠️ **Attribution** - You must give appropriate credit to both Folkets Lexikon and this project

---

<div align="center">

**Made with ❤️ for the Swedish language learning community**

[Report Bug](../../issues) • [Request Feature](../../issues) • [Discuss](../../discussions)

</div>