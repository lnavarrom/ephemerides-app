/**
 * Sistema d'internacionalització (i18n)
 */
class I18n {
    constructor() {
        this.currentLanguage = 'ca';
        this.translations = {};
        this.apiClient = new ApiClient();
    }

    /**
     * Carrega traduccions per un idioma
     */
    async loadLanguage(language) {
        try {
            this.translations = await this.apiClient.getTranslations(language);
            this.currentLanguage = language;
            this.updatePage();
            return true;
        } catch (error) {
            console.error(`Error loading language ${language}:`, error);
            return false;
        }
    }

    /**
     * Obté una traducció per clau
     */
    t(key) {
        const keys = key.split('.');
        let value = this.translations;

        for (const k of keys) {
            value = value?.[k];
        }

        return value || key;
    }

    /**
     * Actualitza tots els elements de la pàgina amb data-i18n
     */
    updatePage() {
        const elements = document.querySelectorAll('[data-i18n]');

        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);

            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });

        // Actualitzar l'atribut lang de l'HTML
        document.documentElement.lang = this.currentLanguage;
    }

    /**
     * Formata la data actual segons l'idioma
     */
    formatCurrentDate() {
        const now = new Date();
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };

        return now.toLocaleDateString(this.currentLanguage, options);
    }
}
