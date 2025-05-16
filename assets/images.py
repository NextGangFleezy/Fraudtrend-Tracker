def get_image_url(category, index=0):
    """
    Get the URL for a stock image based on category and index.
    
    Parameters:
    -----------
    category : str
        The category of image ('fraud investigation', 'data visualization', 'cybersecurity')
    index : int
        The index of the image within the category (0-3)
        
    Returns:
    --------
    str
        URL of the stock image
    """
    # Define image URLs by category
    image_urls = {
        "fraud investigation": [
            "https://pixabay.com/get/g373450be01f0db18bb673e4bfa3a95420cbef55d3207f24d91843f9e8421386f0be4d6dca7882f71ddb1d6a13834a4af0f61e268d9f431d9bc845e097d4e86af_1280.jpg",
            "https://pixabay.com/get/gc6a2ea20c81407dabf705c23273cb8843f6c0b806fe57576055e8182ae8b213fff87ba5cd569e8e754198ea4174bab7bbbb42521b4c6386d88fb4ff2a22b2153_1280.jpg",
            "https://pixabay.com/get/g125f416a723803d62defbea917ec3c5d685f7b0ab557cf18ead048a5c938fcdad21878cf8c116ef55bfdaf6b8a5f7d2220f3c012478fd07982b3c1d9c438b273_1280.jpg",
            "https://pixabay.com/get/g19ede71803ac12f0b25b89e0e154beee09b15b45a633dafc2268f56e370b16fd029431de8b7619b9768eedb4eac35271d426ea740ca66a73dc928d6971759a7d_1280.jpg"
        ],
        "data visualization": [
            "https://pixabay.com/get/g4cc8955df3acc0bfda3622fc72178e0c9f97e738e45f52b0f615fa3a4a3e1d99388ffe84a25226d226895afa034b695b68c543fb1b6bd6422f3ddb8b7fd32194_1280.jpg",
            "https://pixabay.com/get/gfe7b9b97544ea1c5db52800f5bcbef226a2d8704fb96807c0d88c1bc1158cc07d6b92ef0f868b299f1d579ea18e9625a45095fbf6bf09de9de7e6462d3987900_1280.jpg",
            "https://pixabay.com/get/gf3c0e16bb4c5cc1d7aec458ba59392dc23bfff619642aa16c1995d87871afc10975925e6d0136649842abf75c2eaf2ade836c640010b978ab2dbdc076815a528_1280.jpg",
            "https://pixabay.com/get/g33f9b2e8c6766f6fc6dcac2799788d2d5cf12e6a8892f2f97a8335fe9e69097417a283e60b18d296bd9928ecb2506fc63e6c85a152e73bc288c51be666b830ca_1280.jpg"
        ],
        "cybersecurity": [
            "https://pixabay.com/get/g2c5b38d9e424891fc37f4b4af04c3f27cc9a145f6c7ef03f64ee780d2183727ca135319fc94e1b4b0d64250f9c7362887867ff30856a278447adca245f815015_1280.jpg",
            "https://pixabay.com/get/g891fc36df7c0e9e3c1cd88650336379ed1b9f5612619891e9d92c42bfed63ed73dc62df3c675a3140c1aa48226cb01bb2399290dc6c47b028e141f30375edc9a_1280.jpg",
            "https://pixabay.com/get/g1bee7ac2a2684e16c5806fedda34694e0561bb3b38f84137784ba3a480ab467b16b0a8239335ac3a8dc0254e24d6ead5efb04fc0db1c41e45575831ebe263fa0_1280.jpg",
            "https://pixabay.com/get/ge658e1c64bf9712dc51c8cf34840df0ae8856ab965872f04678bed45fc55d4714795b989e1e9cc473ae1988361b14293e8255d4341bd4e0748b0a638e18877ad_1280.jpg"
        ]
    }
    
    # Return the URL for the requested image
    category = category.lower()
    if category in image_urls and 0 <= index < len(image_urls[category]):
        return image_urls[category][index]
    
    # Return a default URL if the requested category or index is not available
    return image_urls["cybersecurity"][0]
