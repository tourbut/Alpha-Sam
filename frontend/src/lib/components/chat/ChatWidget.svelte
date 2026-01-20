<script lang="ts">
    import { Button } from "flowbite-svelte";
    import { auth } from "$lib/stores/auth.svelte";
    import { tick } from "svelte";

    let isOpen = $state(false);
    let message = $state("");
    let chatContainer: HTMLElement;

    // Message type definition
    type Message = {
        id: string;
        text: string;
        sender: "user" | "bot";
        timestamp: Date;
    };

    // Initialize with a welcome message
    let messages = $state<Message[]>([
        {
            id: "1",
            text: "안녕하세요! Alpha-Sam 도우미입니다 무엇을 도와드릴까요?",
            sender: "bot",
            timestamp: new Date(),
        },
    ]);

    function toggleChat() {
        isOpen = !isOpen;
        if (isOpen) {
            scrollToBottom();
        }
    }

    async function sendMessage() {
        if (!message.trim()) return;

        // Add user message
        const userMsg: Message = {
            id: Date.now().toString(),
            text: message,
            sender: "user",
            timestamp: new Date(),
        };
        messages.push(userMsg);
        message = ""; // input clear
        await scrollToBottom();

        // Simulate Bot typing/reply
        setTimeout(async () => {
            const botMsg: Message = {
                id: (Date.now() + 1).toString(),
                text: "이것은 Mock 봇의 자동 응답입니다. 현재 실제 AI 연결은 되어있지 않습니다.",
                sender: "bot",
                timestamp: new Date(),
            };
            messages.push(botMsg);
            await scrollToBottom();
        }, 1000);
    }

    async function scrollToBottom() {
        await tick();
        if (chatContainer) {
            chatContainer.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: "smooth",
            });
        }
    }
</script>

{#if auth.isAuthenticated}
    <div class="fixed bottom-6 right-6 z-50 flex flex-col items-end">
        <!-- Chat Icon Button -->
        <button
            onclick={toggleChat}
            class="bg-gradient-to-r from-purple-600 to-blue-500 hover:from-purple-700 hover:to-blue-600 text-white p-4 rounded-full shadow-lg transition-transform hover:scale-105 active:scale-95 focus:outline-none focus:ring-4 focus:ring-purple-300 dark:focus:ring-purple-900"
            aria-label="Open Chat"
        >
            {#if isOpen}
                <svg
                    class="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M6 18L18 6M6 6l12 12"
                    ></path>
                </svg>
            {:else}
                <svg
                    class="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                    ></path>
                </svg>
            {/if}
        </button>

        <!-- Chat Popover Window -->
        {#if isOpen}
            <div
                class="mb-4 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden flex flex-col transition-all duration-200 origin-bottom-right"
            >
                <!-- Header -->
                <div class="bg-primary-600 p-4 text-white">
                    <h3 class="font-bold text-lg">AI Assistant</h3>
                    <p class="text-xs opacity-80">Alpha-Sam 도우미</p>
                </div>

                <!-- Body -->
                <div
                    class="p-4 h-80 overflow-y-auto bg-gray-50 dark:bg-gray-900 space-y-3"
                    bind:this={chatContainer}
                >
                    {#each messages as msg (msg.id)}
                        <div
                            class="flex w-full {msg.sender === 'user'
                                ? 'justify-end'
                                : 'justify-start'}"
                        >
                            <div
                                class="max-w-[85%] p-3 rounded-lg text-sm
                  {msg.sender === 'user'
                                    ? 'bg-primary-600 text-white rounded-tr-none'
                                    : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-tl-none'}"
                            >
                                <p>{msg.text}</p>
                                <span
                                    class="text-xs opacity-70 block text-right mt-1"
                                >
                                    {msg.timestamp.toLocaleTimeString([], {
                                        hour: "2-digit",
                                        minute: "2-digit",
                                    })}
                                </span>
                            </div>
                        </div>
                    {/each}
                </div>

                <!-- Footer (Input) -->
                <div
                    class="p-3 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800"
                >
                    <form
                        class="flex gap-2"
                        onsubmit={(e) => {
                            e.preventDefault();
                            sendMessage();
                        }}
                    >
                        <input
                            type="text"
                            bind:value={message}
                            placeholder="메시지 입력..."
                            class="flex-1 text-sm rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white px-3 py-2 focus:ring-primary-500 focus:border-primary-500"
                        />
                        <Button
                            type="submit"
                            size="xs"
                            color="blue"
                            class="px-3"
                            disabled={!message.trim()}
                        >
                            전송
                        </Button>
                    </form>
                </div>
            </div>
        {/if}
    </div>
{/if}
