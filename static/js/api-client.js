/**
 * Client per comunicar-se amb el backend Flask
 */
class ApiClient {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }

    /**
     * Obté una efemèride aleatòria del dia actual
     */
    async getTodayEphemeris(language = 'ca') {
        try {
            const response = await fetch(`${this.baseUrl}/api/ephemeris/today?lang=${language}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching ephemeris:', error);
            throw error;
        }
    }

    /**
     * Obté detalls ampliats d'una efemèride
     */
    async getEphemerisDetails(year, text, language = 'ca') {
        try {
            const response = await fetch(`${this.baseUrl}/api/ephemeris/details`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ year, text, lang: language })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching details:', error);
            throw error;
        }
    }

    /**
     * Obté traduccions per un idioma
     */
    async getTranslations(language) {
        try {
            const response = await fetch(`${this.baseUrl}/api/translations/${language}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching translations:', error);
            throw error;
        }
    }
}
