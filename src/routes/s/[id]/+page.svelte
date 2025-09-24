<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import dayjs from 'dayjs';
	import localizedFormat from 'dayjs/plugin/localizedFormat';
	import { toast } from 'svelte-sonner';

	import { WEBUI_NAME } from '$lib/stores';
	import { convertMessagesToHistory } from '$lib/utils';
	import { getChatByShareId, cloneSharedChatById } from '$lib/apis/chats';
	import { getUserById } from '$lib/apis/users';

	dayjs.extend(localizedFormat);

	// Tipos definidos localmente para resolver erros de importação
	interface Message {
		id: string;
		role: 'user' | 'assistant';
		content: string;
		[key: string]: any;
	}

	interface History {
		messages: Record<string, Message>;
		currentId: string | null;
	}

	interface User {
		id: string;
		name: string;
		email: string;
		profile_image_url: string;
		role: 'user' | 'admin';
	}

	interface ChatData {
		id: string;
		user_id: string;
		chat: {
			models?: string[];
			history?: History;
			messages?: Message[];
			title: string;
			timestamp: string;
		};
	}

	let loaded = false;

	let chat: ChatData | null = null;
	let user: User | null = null;
	let title = '';

	onMount(async () => {
		const shareId = $page.params.id;
		if (shareId) {
			if (await loadSharedChat(shareId)) {
				await tick();
				loaded = true;
			} else {
				toast.error('Não foi possível carregar o chat partilhado.');
				await goto('/');
			}
		}
	});

	const loadSharedChat = async (id: string) => {
		try {
			// Assumimos que localStorage.token existe para este protótipo
			const token = localStorage.getItem('token') ?? '';
			const fetchedChat = await getChatByShareId(token, id);
			if (!fetchedChat || !fetchedChat.chat) return false;

			chat = fetchedChat;
			const fetchedUser = await getUserById(token, fetchedChat.user_id);

			if (fetchedUser) {
				user = { ...fetchedUser, role: fetchedUser.role || 'user' };
			}

			const chatContent = fetchedChat.chat;
			title = chatContent.title;

			await tick();
			return true;
		} catch (error) {
			console.error(error);
			return false;
		}
	};

	const cloneSharedChat = async () => {
		if (!chat) return;
		const token = localStorage.getItem('token') ?? '';
		const res = await cloneSharedChatById(token, chat.id).catch((error) => {
			toast.error(`${error}`);
			return null;
		});

		if (res) {
			goto(`/c/${res.id}`);
		}
	};
</script>

<svelte:head>
	<title>
		{title ? `${title.length > 30 ? `${title.slice(0, 30)}...` : title} • ${$WEBUI_NAME}` : `${$WEBUI_NAME}`}
	</title>
</svelte:head>

{#if loaded && chat && user}
	<div
		class="h-screen max-h-[100dvh] w-full flex flex-col text-gray-700 dark:text-gray-100 bg-white dark:bg-gray-900"
	>
		<div class="flex flex-col flex-auto justify-center relative p-8">
			<div class="pt-5 px-2 w-full max-w-5xl mx-auto text-center">
				<h1 class="text-3xl font-bold mb-2">{title}</h1>
				<p class="text-gray-400">
					Partilhado por {user.name} em {dayjs(chat.chat.timestamp).format('LLL')}
				</p>

				<div class="mt-8">
					<button
						class="px-6 py-3 text-sm font-medium bg-black hover:bg-gray-800 text-white dark:bg-white dark:text-black dark:hover:bg-gray-200 transition rounded-full"
						on:click={cloneSharedChat}
					>
						Clonar Chat
					</button>
				</div>
			</div>
		</div>
	</div>
{:else}
	<div class="flex h-screen w-full items-center justify-center bg-gray-100 dark:bg-gray-900">
		<p class="text-gray-500">A carregar chat partilhado...</p>
	</div>
{/if}

