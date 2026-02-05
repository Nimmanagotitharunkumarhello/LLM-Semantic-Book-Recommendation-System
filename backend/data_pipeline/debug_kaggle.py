try:
    from kagglehub import dataset_download
    print("Imported dataset_download successfully")
except ImportError as e:
    print(f"Import failed: {e}")
    import kagglehub
    # Check if it's under datasets
    try:
        from kagglehub.datasets import dataset_download
        print("Imported from kagglehub.datasets")
    except ImportError:
        print("Not in kagglehub.datasets either")
