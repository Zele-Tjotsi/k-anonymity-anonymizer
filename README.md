# 🛡️ k-Anonymity Anonymizer

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://k-anonymity-anonymizer.streamlit.app)

**Protect individual privacy while keeping data useful for analysis.**

## 🚀 Live Demo

**Try it now:** [https://k-anonymity-anonymizer.streamlit.app](https://k-anonymity-anonymizer.streamlit.app)

No installation needed. Upload a CSV and see k-anonymity in action.

## 🎯 Problem It Solves

Organizations need to share data (patient records, customer transactions) without exposing individuals. k-Anonymity is a proven privacy model that ensures each person's data is indistinguishable from at least k-1 others.

## ✨ Features

- 📁 Upload CSV or Excel files
- 🔍 Select quasi-identifier columns (Age, Zip Code, Gender, etc.)
- 🎛️ Set your desired k value (2-10)
- 🔒 Automatic generalization for numeric columns
- 🚫 Suppression for rare categorical values
- 📊 Visual before/after comparison
- 💾 Download anonymized data
- 📈 Displays achieved vs. target k-anonymity

## 📖 How It Works

**Before Anonymization:**
| Age | ZipCode | Gender |
|-----|---------|--------|
| 25  | 10001   | M      |
| 25  | 10001   | M      |
| 25  | 10001   | F      |

**After k=2 Anonymization:**
| Age | ZipCode | Gender |
|-----|---------|--------|
| 0   | 0       | M      |
| 0   | 0       | M      |
| 0   | 0       | Other  |

Now each row is indistinguishable from at least 1 other row → k=2 anonymity.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Data Processing:** Pandas, NumPy
- **File Support:** CSV, Excel (openpyxl)

## 📊 Use Cases

- 🏥 **Healthcare:** Share patient data for research without violating HIPAA
- 💰 **Finance:** Analyze transaction patterns while protecting customers
- 📈 **Marketing:** Segment users without exposing individuals
- 🎓 **Academia:** Release research datasets ethically

## 🔄 Future Improvements

- [ ] Differential privacy integration
- [ ] l-diversity and t-closeness metrics
- [ ] Re-identification attack simulation
- [ ] Support for larger datasets (100k+ rows)

## 📝 License

MIT License - Free for commercial and personal use.

## 👤 Author

**Zele Tjotsi** - BSc Computer Science, National University of Lesotho

[GitHub](https://github.com/Zele-Tjotsi) | [LinkedIn](https://linkedin.com/in/zele-tjotsi) | [Email](mailto:your-email@example.com)

## 🙏 Acknowledgments

- Samarati, P. and Sweeney, L. (2002) - k-Anonymity research papers
- Streamlit for the amazing framework
