const { createApp, ref, computed } = Vue;
const { createVuetify } = Vuetify;

const vuetify = createVuetify({
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme: {
        colors: {
          primary: '#9EBF74',
          secondary: '#FFEFB2',
          accent: '#FD7D00',
          background: '#FFFFFF',
        },
      },
    },
  },
});

createApp({
  setup() {
    const userQuery = ref('');
    const chatMessages = ref([
      {
        role: 'bot',
        text: 'Hallo 👋! Ich bin NutriBot, dein digitaler Ernährungsexperte von nurec. Wie kann ich dir helfen? 🥗🍎',
      },
    ]);
    const loading = ref(false);

    const askQuestion = async () => {
      if (!userQuery.value.trim()) {
        return;
      }

      chatMessages.value.push({ role: 'user', text: userQuery.value });

      // Temporäres "Schreibt"-Icon hinzufügen
      chatMessages.value.push({ role: 'bot', text: '...', temporary: true });

      loading.value = true;
      const question = userQuery.value;
      userQuery.value = '';

      try {
        const res = await fetch('http://127.0.0.1:5001/query', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ user_query: question }),
        });

        const data = await res.json();
        
        // Temporäre Nachricht entfernen
        chatMessages.value = chatMessages.value.filter(msg => !msg.temporary);

        if (res.ok) {
          chatMessages.value.push({ role: 'bot', text: data.response || 'Keine Antwort erhalten.' });
        } else {
          chatMessages.value.push({ role: 'bot', text: `Fehler: ${data.error || 'Unbekannter Fehler'}` });
        }
      } catch (error) {
        chatMessages.value = chatMessages.value.filter(msg => !msg.temporary);
        chatMessages.value.push({ role: 'bot', text: `Fehler beim Abrufen der Antwort: ${error.message}` });
      } finally {
        loading.value = false;
      }
    };

    return {
      userQuery,
      chatMessages,
      loading,
      askQuestion,
    };
  },
}).use(vuetify).mount('#app');
