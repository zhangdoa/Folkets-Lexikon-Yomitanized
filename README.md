# 📚 Folkets Lexikon for Yomitan

[![Build Dictionary](https://github.com/zhangdoa/Folkets-Lexikon-Yomitanized/actions/workflows/build-dictionary.yml/badge.svg)](https://github.com/zhangdoa/Folkets-Lexikon-Yomitanized/actions/workflows/build-dictionary.yml)

A comprehensive Yomitan dictionary built from the authoritative [Folkets Lexikon](https://folkets-lexikon.csc.kth.se/folkets/om.en.html) Swedish-English database maintained by KTH Royal Institute of Technology.

## 🚀 Quick Download

1. Navigate to [**Actions**](../../actions/workflows/build-dictionary.yml)
2. Click **"Run workflow"** → **"Run workflow"** (green button)
3. Wait 2-3 minutes for build completion
4. Download the generated `folkets-lexikon-yomitan-v*.zip` file from Artifacts

## 📱 Installation in Yomitan

1. **Download** the dictionary ZIP file
2. **Open** Yomitan extension settings (click the extension icon → settings gear)
3. **Navigate** to **"Dictionaries"** in the left sidebar
4. **Click** **"Import"** button
5. **Select** the downloaded ZIP file
6. **Enable** the dictionary by toggling it on
7. **Enjoy** instant Swedish translations!

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