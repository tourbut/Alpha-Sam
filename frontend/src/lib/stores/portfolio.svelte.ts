import { fetchPortfolios, fetchPortfolioPositions, createPortfolio, type Portfolio, type PortfolioCreate } from "$lib/apis/portfolio"
import { browser } from "$app/environment"

class PortfolioStore {
    portfolios = $state<Portfolio[]>([])
    selectedPortfolioId = $state<string | null>(null)
    positions = $state<any[]>([])
    loading = $state(false)

    // Computed: Get select portfolio object
    selectedPortfolio = $derived(
        this.portfolios.find((p) => p.id === this.selectedPortfolioId) || null
    )

    constructor() {
        if (browser) {
            const storedId = localStorage.getItem("selectedPortfolioId")
            if (storedId) {
                this.selectedPortfolioId = storedId
            }
        }
    }

    async loadPortfolios() {
        this.loading = true
        try {
            this.portfolios = await fetchPortfolios()

            // Auto-select first if none selected or selected invalid
            if (this.portfolios.length > 0) {
                if (!this.selectedPortfolioId || !this.portfolios.find(p => p.id === this.selectedPortfolioId)) {
                    this.selectPortfolio(this.portfolios[0].id)
                } else {
                    // If already selected, reload positions
                    await this.loadPositions(this.selectedPortfolioId)
                }
            }
        } catch (e) {
            console.error("Failed to load portfolios", e)
        } finally {
            this.loading = false
        }
    }

    async selectPortfolio(id: string) {
        this.selectedPortfolioId = id
        if (browser) {
            localStorage.setItem("selectedPortfolioId", String(id))
        }
        await this.loadPositions(id)
    }

    async loadPositions(id: string) {
        this.loading = true
        try {
            this.positions = await fetchPortfolioPositions(id)
        } catch (e) {
            console.error("Failed to load positions", e)
            this.positions = []
        } finally {
            this.loading = false
        }
    }

    async addPortfolio(data: PortfolioCreate) {
        this.loading = true
        try {
            const newPortfolio = await createPortfolio(data)
            await this.loadPortfolios()
            this.selectPortfolio(newPortfolio.id)
            return newPortfolio
        } catch (e) {
            console.error("Failed to create portfolio", e)
            throw e
        } finally {
            this.loading = false
        }
    }
}

export const portfolioStore = new PortfolioStore()
