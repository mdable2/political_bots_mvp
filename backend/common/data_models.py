from typing import Set, List


class TranscriptObject():
    keywords: Set[str]
    text: str
    speaker: str

    def __init__(self, keywords, text, speaker) -> None:
        self.keywords = keywords
        self.text = text
        self.speaker = speaker

    def __repr__(self) -> str:
        return f"TranscriptObject()\nkeywords: {self.keywords}\nspeaker: {self.speaker}\ntext: {self.text}\n"
    
    def __str__(self) -> str:
        return f"keywords: {self.keywords}\nspeaker: {self.speaker}\ntext: {self.text}\n"

class TranscriptPage():
    title: str
    keywords: Set[str]
    speakers: Set[str]
    transcript_objects: List[TranscriptObject]

    def __init__(self, title, keywords, speakers, transcript_objects) -> None:
        self.title = title
        self.keywords = keywords
        self.speakers = speakers
        self.transcript_objects = transcript_objects
    
    def __repr__(self) -> str:
        return f"TranscriptPage()\ntitle: {self.title}\nkeywords: {self.keywords}\nspeakers: {self.speakers}\ntranscript_objects: {self.transcript_objects}\n"
    
    def __str__(self) -> str:
        return f"title: {self.title}\nkeywords: {self.keywords}\nspeakers: {self.speakers}\ntranscript_objects: {self.transcript_objects}\n"     
