# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

from azure.ai.assistant.management.base_ai_client import BaseAiClient

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

class AzureInferenceClient(BaseAiClient):
    """
    A class that manages Azure Inference Clients

    :param client_args: Additional keyword arguments for configuring the client.
    :type client_args: Dict
    """
    def __init__(self, **client_args) -> None:
        super().__init__(ChatCompletionsClient(
            credential=AzureKeyCredential(client_args.get('key')), 
            headers={"api-key": client_args.get('key')}, 
            **client_args,
        ))
    
    def create_completions(self, **kwargs):
        """
        Creates completions using the Azure inference service.

        :param kwargs: Keyword arguments for the completion request.
        :return: Completion results from the Azure inference service.
        """
        if "timeout" in kwargs and kwargs["timeout"] is None:
            kwargs.pop("timeout")

        for message in kwargs.get("messages"):
            if isinstance(message.get("content"), list):
                is_text_only = all(content.get("type") == "text" for content in message.get("content") if message.get("content"))
                if is_text_only:
                    message["content"] = "".join((content.get("text") for content in message.get("content")))

        return self._ai_client.complete(**kwargs)
    
    @property
    def ai_client(self):
        """
        Returns the underlying AI client.

        :return: The AI client.
        :rtype: ChatCompletionsClient
        """
        return self._ai_client