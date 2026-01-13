/**
 * Social Features를 위한 상태 관리 스토어 (Svelte 5 Runes)
 */
export interface LeaderboardEntry {
    user_id: number;
    nickname: string;
    pnl_percent: number;
    rank: number;
}

export interface ShareSettings {
    show_amounts: boolean;
    show_pnl: boolean;
    show_weights: boolean;
}

class SocialStore {
    // 리더보드 데이터 ($state)
    leaderboard = $state<LeaderboardEntry[]>([]);
    loading = $state(false);

    // 공유 설정 ($state)
    shareSettings = $state<ShareSettings>({
        show_amounts: false,
        show_pnl: true,
        show_weights: true
    });

    /**
     * 리더보드 데이터 로드 (현재는 Mock 데이터)
     */
    async loadLeaderboard() {
        this.loading = true;
        try {
            // TODO: 실제 API 연동 후 교체
            // const response = await getLeaderboard();

            // Mock 데이터 시뮬레이션
            await new Promise(resolve => setTimeout(resolve, 500));
            this.leaderboard = [
                { user_id: 101, nickname: "WealthWizard", pnl_percent: 45.2, rank: 1 },
                { user_id: 202, nickname: "BullRider", pnl_percent: 32.8, rank: 2 },
                { user_id: 303, nickname: "AlphaTrader", pnl_percent: 28.5, rank: 3 },
                { user_id: 404, nickname: "CoinKing", pnl_percent: 15.2, rank: 4 },
                { user_id: 505, nickname: "HODLer", pnl_percent: 12.0, rank: 5 },
            ];
        } catch (e) {
            console.error("Failed to load leaderboard:", e);
        } finally {
            this.loading = false;
        }
    }

    /**
     * 포트폴리오 공유 링크 생성 (현재는 Mock UUID)
     */
    async createShareLink(): Promise<string> {
        // TODO: 실제 API 연동 (POST /portfolio/share)
        console.log("Creating share link with settings:", this.shareSettings);
        await new Promise(resolve => setTimeout(resolve, 300));
        return `https://alpha-sam.io/portfolio/v/${self.crypto.randomUUID()}`;
    }
}

export const socialStore = new SocialStore();
