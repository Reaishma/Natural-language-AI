"""
NLTK Data Setup Script
Downloads all required NLTK and TextBlob corpora for the NLP Virtual Assistant
"""
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    """Download all required NLTK data packages"""
    packages = [
        'punkt',
        'punkt_tab',
        'stopwords',
        'averaged_perceptron_tagger',
        'averaged_perceptron_tagger_eng',
        'maxent_ne_chunker',
        'maxent_ne_chunker_tab',
        'words',
        'brown',
        'wordnet',
        'conll2000',
        'movie_reviews'
    ]
    
    print("Downloading NLTK data packages...")
    for package in packages:
        try:
            nltk.download(package, quiet=True)
            print(f"✓ {package}")
        except Exception as e:
            print(f"✗ {package}: {str(e)}")
    
    print("\nNLTK data download complete!")

def download_textblob_corpora():
    """Download TextBlob corpora"""
    import subprocess
    print("\nDownloading TextBlob corpora...")
    try:
        subprocess.run(["python", "-m", "textblob.download_corpora"], check=True)
        print("✓ TextBlob corpora downloaded")
    except Exception as e:
        print(f"✗ TextBlob corpora download failed: {str(e)}")

if __name__ == "__main__":
    download_nltk_data()
    download_textblob_corpora()
    print("\n✅ All NLP data packages installed successfully!")
