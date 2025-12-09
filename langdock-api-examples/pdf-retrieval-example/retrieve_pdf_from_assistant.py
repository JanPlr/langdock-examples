import requests
import json
from typing import Optional, List, Dict


class LangdockClient:
    def __init__(self, api_key: str, base_url: str = "https://api.langdock.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_conversation(self, assistant_id: str) -> Optional[str]:
        print(f"[DEBUG] Creating conversation for assistant: {assistant_id}")
        url = f"{self.base_url}/conversation/v1/create"
        payload = {"assistantId": assistant_id}
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            conversation_id = result.get("conversationId") or result.get("id")
            print(f"[DEBUG] Conversation created: {conversation_id}")
            return conversation_id
        except requests.exceptions.HTTPError as e:
            print(f"[DEBUG] Failed to create conversation: {e}")
            if e.response:
                print(f"[DEBUG] Response: {e.response.text}")
            print("[DEBUG] Will try to extract conversation ID from assistant response")
            return None
        except Exception as e:
            print(f"[DEBUG] Unexpected error creating conversation: {e}")
            return None
    
    def call_assistant(self, assistant_id: str, message: str, conversation_id: Optional[str] = None) -> Dict:
        print(f"[DEBUG] Calling assistant: {assistant_id}")
        if conversation_id:
            print(f"[DEBUG] Using conversation ID: {conversation_id}")
        url = f"{self.base_url}/assistant/v1/chat/completions"
        payload = {
            "assistantId": assistant_id,
            "messages": [{"role": "user", "content": message}]
        }
        if conversation_id:
            payload["conversationId"] = conversation_id
        
        print(f"[DEBUG] Request payload: {json.dumps(payload, indent=2)}")
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"[DEBUG] Response status: {response.status_code}")
        return result
    
    def extract_conversation_id(self, response: Dict) -> Optional[str]:
        print("[DEBUG] Extracting conversation ID from response...")
        conversation_id = response.get("conversationId") or response.get("conversation_id")
        if conversation_id:
            print(f"[DEBUG] Found conversation ID in response root: {conversation_id}")
            return conversation_id
        if "choices" in response and len(response["choices"]) > 0:
            choice = response["choices"][0]
            conversation_id = choice.get("conversationId") or choice.get("conversation_id")
            if conversation_id:
                print(f"[DEBUG] Found conversation ID in choice: {conversation_id}")
                return conversation_id
        print("[DEBUG] No conversation ID found in response")
        return None
    
    def extract_attachments(self, response: Dict) -> List[Dict]:
        print("[DEBUG] Extracting attachments from response...")
        attachments = []
        if "choices" in response and len(response["choices"]) > 0:
            choice = response["choices"][0]
            if "message" in choice and "attachments" in choice["message"]:
                attachments.extend(choice["message"]["attachments"])
                print(f"[DEBUG] Found {len(attachments)} attachment(s)")
            else:
                print("[DEBUG] No attachments found in message")
        else:
            print("[DEBUG] No choices found in response")
        return attachments
    
    def download_attachment(self, attachment_id: str) -> bytes:
        print(f"[DEBUG] Downloading attachment: {attachment_id}")
        url = f"{self.base_url}/attachment/v1/{attachment_id}/download"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content_length = len(response.content)
        print(f"[DEBUG] Downloaded {content_length} bytes")
        return response.content


def main():
    API_KEY = "sk-nDMlep264pR79Vfjfab7E36YNw19V1CeCeuRoSfNJC4pciAcK5-5jasr9fv0knopIx3oknerI_pV2Pjtq8I_1w"
    ASSISTANT_ID = "b7d73d1e-5522-4e17-86be-6d4256c11a1d"
    
    print("=" * 60)
    print("Langdock PDF Retrieval - Debug Mode")
    print("=" * 60)
    
    client = LangdockClient(API_KEY)
    
    print("\n[STEP 1] Creating conversation...")
    conversation_id = client.create_conversation(ASSISTANT_ID)
    
    print("\n[STEP 2] Calling assistant...")
    try:
        response = client.call_assistant(ASSISTANT_ID, "Please generate a PDF document for me", conversation_id)
        
        print("\n[DEBUG] Full API Response:")
        print(json.dumps(response, indent=2))
        
        if not conversation_id:
            print("\n[STEP 2.5] Extracting conversation ID from response...")
            conversation_id = client.extract_conversation_id(response)
        
        print("\n[STEP 3] Extracting attachments...")
        attachments = client.extract_attachments(response)
        
        if not attachments:
            print("\n[ERROR] No attachments found in response!")
            print("[DEBUG] The assistant may need to be configured to output attachments.")
            return
        
        print(f"\n[STEP 4] Processing {len(attachments)} attachment(s)...")
        for idx, attachment in enumerate(attachments, 1):
            print(f"\n--- Attachment {idx} ---")
            attachment_id = attachment.get("attachmentId")
            attachment_name = attachment.get("name", "unknown")
            attachment_type = attachment.get("type", "unknown")
            print(f"ID: {attachment_id}")
            print(f"Name: {attachment_name}")
            print(f"Type: {attachment_type}")
            
            if not attachment_id:
                print(f"[ERROR] No attachmentId found for attachment {idx}")
                continue
            
            try:
                pdf_content = client.download_attachment(attachment_id)
                filename = attachment.get("name", f"generated_pdf_{idx}.pdf")
                if not filename.endswith(".pdf"):
                    filename = f"{filename}.pdf"
                
                with open(filename, "wb") as f:
                    f.write(pdf_content)
                print(f"[SUCCESS] Saved PDF: {filename}")
            except requests.exceptions.HTTPError as e:
                print(f"[ERROR] Failed to download attachment: {e}")
                if e.response:
                    print(f"[DEBUG] Response status: {e.response.status_code}")
                    print(f"[DEBUG] Response body: {e.response.text[:500]}")
            except Exception as e:
                print(f"[ERROR] Unexpected error: {e}")
        
        print("\n" + "=" * 60)
        print("Process completed!")
        print("=" * 60)
    
    except requests.exceptions.HTTPError as e:
        print(f"\n[ERROR] Failed to call assistant: {e}")
        if e.response:
            print(f"[DEBUG] Response status: {e.response.status_code}")
            print(f"[DEBUG] Response body: {e.response.text}")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
