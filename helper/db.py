from supabase import create_client, Client


class DB:
    def __init__(self, url, key):
        self.__db: Client = create_client(url, key)

    def __check_author(self, email: str):
        try:
            author, _ = (
                self.__db.table("authors").select("*").eq("email", email).execute()
            )
            if len(author[1]) == 0:
                return False, "Author not found"
            return True, author[1][0]
        except Exception:
            return False, "Failed to check author"

    def __create_author(self, data: dict):
        print("[DATA]", data)
        try:
            author, _ = self.__db.table("authors").insert(data).execute()
            if len(author[1]) == 0:
                return False, "Failed to create author"
            return True, author[1][0]
        except Exception:
            return False, "Failed to create author. Please try again later"

    def __check_tts(self, uuid: str):
        try:
            tts, _ = (
                self.__db.table("crosswords").select("*").eq("uuid", uuid).execute()
            )
            if len(tts[1]) == 0:
                return False, "TTS not found"
            return True, tts[1][0]
        except Exception:
            return False, "Failed to check TTS"

    def __create_tts(self, data: dict):
        try:
            tts, _ = self.__db.table("crosswords").insert(data).execute()
            if len(tts[1]) == 0:
                return False, "Failed to create TTS"
            return True, tts[1][0]
        except Exception:
            return False, "Failed to create TTS. Please try again later"

    def __update_tts(self, uuid: str, data: dict):
        try:
            tts, _ = (
                self.__db.table("crosswords").update(data).eq("uuid", uuid).execute()
            )
            if len(tts[1]) == 0:
                return False, "Failed to update TTS"
            return True, tts[1][0]
        except Exception:
            return False, "Failed to update TTS. Please try again later"

    def submit(self, author_input, tts_input):
        # check author. if not exist, create new author
        is_author_exist, author = self.__check_author(author_input["email"])
        author_id = author["id"] if is_author_exist else None
        if not is_author_exist:
            is_author_created, author = self.__create_author(author_input)
            if not is_author_created:
                return False, author

        # check tts. if not exist, create new tts
        if author_id is not None:
            tts_input["author_id"] = author_id

        is_tts_exist, tts = self.__check_tts(tts_input["uuid"])
        if not is_tts_exist:
            is_tts_created, tts = self.__create_tts(tts_input)
            print("[TTS]", is_tts_created, tts)
            if not is_tts_created:
                return False, tts

        # update tts
        is_tts_updated, tts = self.__update_tts(tts_input["uuid"], tts_input)
        if not is_tts_updated:
            return False, tts

        return True, tts
