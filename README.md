# 📚 Folkets Lexikon for Yomitan

A Yomitan dictionary built from the comprehensive [Folkets Lexikon](https://folkets-lexikon.csc.kth.se/folkets/om.en.html) Swedish-English database.

## 🚀 Quick Download

1. Go to [**Actions**](../../actions/workflows/build-dictionary.yml)
2. Click **"Run workflow"** 
3. Wait 2-3 minutes for build completion
4. Download the dictionary ZIP file

## 📱 Installation

1. Download the dictionary file from Actions
2. Open Yomitan extension settings
3. Navigate to **Dictionaries** section
4. Click **Import** and select the downloaded ZIP
5. Enable the dictionary

## ✨ Features

- **Comprehensive**: 100,000+ Swedish-English entries
- **Always Fresh**: Built on-demand from latest Folkets Lexikon data
- **Examples**: Includes usage examples and translations
- **Word Forms**: Complete inflection information

## 🔧 Build Locally

```bash
# Download source data
curl -o folkets_sv_en_public.xml https://folkets-lexikon.csc.kth.se/folkets/folkets_sv_en_public.xml

# Run builder
python __main__.py

## 📄 License

This project and the generated dictionary are licensed under **Creative Commons Attribution-ShareAlike 2.5 Generic** to maintain compatibility with the original Folkets Lexikon data.

### Attribution
- **Original Data**: [Folkets Lexikon](https://folkets-lexikon.csc.kth.se/) by KTH Royal Institute of Technology
- **License**: CC BY-SA 2.5 Generic
- **Conversion**: This community project

### Usage Rights
✅ **Use** - Free for personal and commercial use  
✅ **Modify** - You can adapt and build upon the material  
✅ **Share** - You can distribute the material  
⚠️ **Share Alike** - If you remix or build upon the material, you must distribute under the same license  
⚠️ **Attribution** - You must give appropriate credit to both Folkets Lexikon and this project