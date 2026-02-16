/**
 * Aplicació principal d'efemèrides
 */
class EphemerisApp {
    constructor() {
        this.apiClient = new ApiClient();
        this.i18n = new I18n();
        this.currentEphemeris = null;
        this.detailsExpanded = false;

        this.initElements();
        this.attachEventListeners();
        this.init();
    }

    /**
     * Inicialitza referències als elements del DOM
     */
    initElements() {
        this.currentDateEl = document.getElementById('current-date');
        this.loadingState = document.getElementById('loading-state');
        this.errorState = document.getElementById('error-state');
        this.ephemerisContent = document.getElementById('ephemeris-content');
        this.yearBadge = document.getElementById('year-badge');
        this.ephemerisText = document.getElementById('ephemeris-text');
        this.ephemerisDetails = document.getElementById('ephemeris-details');
        this.detailsThumbnail = document.getElementById('details-thumbnail');
        this.detailsDescription = document.getElementById('details-description');
        this.detailsLinks = document.getElementById('details-links');
        this.nextBtn = document.getElementById('next-btn');
        this.detailsBtn = document.getElementById('details-btn');
        this.retryBtn = document.getElementById('retry-btn');
        this.langButtons = document.querySelectorAll('.lang-btn');
    }

    /**
     * Adjunta event listeners
     */
    attachEventListeners() {
        this.nextBtn.addEventListener('click', () => this.loadNewEphemeris());
        this.detailsBtn.addEventListener('click', () => this.toggleDetails());
        this.retryBtn.addEventListener('click', () => this.loadNewEphemeris());

        this.langButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.changeLanguage(e.target.dataset.lang));
        });
    }

    /**
     * Inicialitza l'aplicació
     */
    async init() {
        // Carregar idioma per defecte
        await this.i18n.loadLanguage('ca');

        // Mostrar data actual
        this.updateCurrentDate();

        // Carregar primera efemèride
        this.loadNewEphemeris();
    }

    /**
     * Actualitza la data actual
     */
    updateCurrentDate() {
        this.currentDateEl.textContent = this.i18n.formatCurrentDate();
    }

    /**
     * Mostra estat de càrrega
     */
    showLoadingState() {
        this.loadingState.classList.remove('hidden');
        this.errorState.classList.add('hidden');
        this.ephemerisContent.classList.add('hidden');
        this.nextBtn.disabled = true;
        this.detailsBtn.disabled = true;
    }

    /**
     * Mostra estat d'error
     */
    showErrorState() {
        this.loadingState.classList.add('hidden');
        this.errorState.classList.remove('hidden');
        this.ephemerisContent.classList.add('hidden');
        Animations.shake(this.errorState);
    }

    /**
     * Mostra contingut de l'efemèride
     */
    showEphemerisContent() {
        this.loadingState.classList.add('hidden');
        this.errorState.classList.add('hidden');
        this.ephemerisContent.classList.remove('hidden');
        Animations.fadeIn(this.ephemerisContent, 600);
        this.nextBtn.disabled = false;
        this.detailsBtn.disabled = !this.currentEphemeris?.hasDetails;
    }

    /**
     * Carrega una nova efemèride
     */
    async loadNewEphemeris() {
        this.showLoadingState();
        this.detailsExpanded = false;
        this.ephemerisDetails.classList.add('hidden');

        try {
            const ephemeris = await this.apiClient.getTodayEphemeris(this.i18n.currentLanguage);
            this.currentEphemeris = ephemeris;

            // Actualitzar UI
            this.yearBadge.textContent = ephemeris.year;
            this.ephemerisText.textContent = ephemeris.text;

            this.showEphemerisContent();
        } catch (error) {
            console.error('Error loading ephemeris:', error);
            this.showErrorState();
        }
    }

    /**
     * Alterna la visualització de detalls
     */
    async toggleDetails() {
        if (this.detailsExpanded) {
            // Tancar detalls
            Animations.fadeOut(this.ephemerisDetails, 300);
            this.detailsBtn.querySelector('span').textContent = this.i18n.t('actions.moreInfo');
            this.detailsExpanded = false;
        } else {
            // Carregar i mostrar detalls
            this.detailsBtn.disabled = true;
            this.detailsBtn.querySelector('span').textContent = this.i18n.t('loading.details');

            try {
                const details = await this.apiClient.getEphemerisDetails(
                    this.currentEphemeris.year,
                    this.currentEphemeris.text,
                    this.i18n.currentLanguage
                );

                // Actualitzar UI amb detalls
                this.detailsDescription.textContent = details.description || '';

                if (details.thumbnail) {
                    this.detailsThumbnail.src = details.thumbnail;
                    this.detailsThumbnail.classList.remove('hidden');
                } else {
                    this.detailsThumbnail.classList.add('hidden');
                }

                // Renderitzar links
                this.detailsLinks.innerHTML = '';
                if (details.links && details.links.length > 0) {
                    details.links.forEach(link => {
                        const a = document.createElement('a');
                        a.href = link.url;
                        a.textContent = `→ ${link.title}`;
                        a.target = '_blank';
                        a.rel = 'noopener noreferrer';
                        this.detailsLinks.appendChild(a);
                    });
                }

                // Mostrar detalls
                this.ephemerisDetails.classList.remove('hidden');
                Animations.fadeIn(this.ephemerisDetails, 400);
                this.detailsBtn.querySelector('span').textContent = this.i18n.t('actions.lessInfo');
                this.detailsExpanded = true;
            } catch (error) {
                console.error('Error loading details:', error);
                alert(this.i18n.t('error.loadingDetails'));
            } finally {
                this.detailsBtn.disabled = false;
            }
        }
    }

    /**
     * Canvia l'idioma de l'aplicació
     */
    async changeLanguage(language) {
        // Actualitzar botons
        this.langButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.lang === language);
        });

        // Carregar nou idioma
        const success = await this.i18n.loadLanguage(language);

        if (success) {
            // Actualitzar data
            this.updateCurrentDate();

            // Recarregar efemèride en nou idioma
            this.loadNewEphemeris();
        }
    }
}

// Inicialitzar l'aplicació quan el DOM estigui llest
document.addEventListener('DOMContentLoaded', () => {
    window.app = new EphemerisApp();
});
