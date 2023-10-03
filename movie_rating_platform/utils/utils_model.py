def custom_title(input_string: str) -> str:
    exceptions = [
        "to",
        "the",
        "of",
        "and",
        "on",
        "a",
        "an",
        "is",
        "but",
        "in",
        "under",
        "over",
        "with",
        "without",
        "or",
        "nor",
        "for",
        "yet",
        "s",
    ]
    words = input_string.lower().split()
    title_case_words = [words[0].title()]
    for word in words[1:]:
        if word not in exceptions:
            title_case_words.append(word.title())
        else:
            title_case_words.append(word)
    return " ".join(title_case_words)
