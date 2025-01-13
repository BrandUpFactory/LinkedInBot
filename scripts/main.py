from scripts.scraper import manage_buffer, cleanup_driver

def main():
    try:
        buffer = manage_buffer(3)
        for idx, post in enumerate(buffer, 1):
            print(f"Beitrag {idx}:")
            print(f"Text: {post['text']}")
            print(f"Profilbild: {post['profile_image']}")
            print(f"Bild: {post['image']}")
            print("-" * 50)
    finally:
        cleanup_driver()

if __name__ == "__main__":
    main()
