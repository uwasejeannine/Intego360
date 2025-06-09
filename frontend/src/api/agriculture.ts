import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

// Type definitions
interface Crop {
  id: number;
  name: string;
  scientific_name: string;
  category: 'cereals' | 'legumes' | 'tubers' | 'vegetables' | 'fruits' | 'cash_crops';
  growing_season: 'season_a' | 'season_b' | 'season_c' | 'year_round';
  growth_period_days: number;
  ideal_rainfall_mm: number;
  ideal_temperature_min: number;
  ideal_temperature_max: number;
  average_yield_per_hectare: number;
  market_price_per_kg: number;
  created_at: string;
  updated_at: string;
}

interface Farmer {
  id: number;
  farmer_id: string;
  first_name: string;
  last_name: string;
  national_id: string;
  date_of_birth: string;
  gender: 'M' | 'F';
  phone_number: string;
  email: string;
  district: number;
  sector: number;
  cell: string;
  village: string;
  total_land_hectares: number;
  farming_experience_years: number;
  education_level: 'none' | 'primary' | 'secondary' | 'vocational' | 'university';
  main_crops: number[];
  is_cooperative_member: boolean;
  cooperative_name: string;
  has_bank_account: boolean;
  bank_name: string;
  account_number: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface Cooperative {
  id: number;
  name: string;
  registration_number: string;
  district: number;
  sector: number;
  phone_number: string;
  email: string;
  physical_address: string;
  chairperson_name: string;
  chairperson_phone: string;
  secretary_name: string;
  treasurer_name: string;
  date_established: string;
  total_members: number;
  active_members: number;
  female_members: number;
  youth_members: number;
  total_assets: number;
  annual_revenue: number;
  primary_activities: string;
  crops_handled: number[];
  is_active: boolean;
  certification_status: 'pending' | 'certified' | 'suspended' | 'revoked';
  created_at: string;
  updated_at: string;
}

interface Season {
  id: number;
  name: 'season_a' | 'season_b' | 'season_c';
  year: number;
  start_date: string;
  end_date: string;
  total_rainfall_mm: number;
  average_temperature: number;
  drought_periods: number;
  flood_incidents: number;
  total_production_tons: number;
  total_area_cultivated: number;
  average_yield: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface Production {
  id: number;
  farmer: number;
  crop: number;
  season: number;
  area_planted_hectares: number;
  planting_date: string;
  seed_variety: string;
  seed_source: 'own' | 'purchased' | 'government' | 'cooperative' | 'ngo';
  fertilizer_used: boolean;
  fertilizer_type: string;
  fertilizer_quantity_kg: number;
  pesticide_used: boolean;
  pesticide_type: string;
  irrigation_used: boolean;
  irrigation_type: string;
  harvest_date: string;
  quantity_harvested_kg: number;
  quality_grade: 'A' | 'B' | 'C' | 'D';
  quantity_consumed_kg: number;
  quantity_sold_kg: number;
  quantity_stored_kg: number;
  quantity_lost_kg: number;
  average_selling_price: number;
  challenges_faced: string;
  pest_diseases: string;
  weather_impact: string;
  created_at: string;
  updated_at: string;
}

interface Extension {
  id: number;
  title: string;
  description: string;
  service_type: 'training' | 'demonstration' | 'advisory' | 'input_supply' | 'market_linkage' | 'technology';
  district: number;
  sectors: number[];
  target_crops: number[];
  target_farmers: number[];
  start_date: string;
  end_date: string;
  venue: string;
  facilitator: string;
  facilitator_organization: string;
  target_participants: number;
  actual_participants: number;
  male_participants: number;
  female_participants: number;
  youth_participants: number;
  budget_allocated: number;
  budget_spent: number;
  materials_provided: string;
  knowledge_gained: string;
  practices_adopted: string;
  feedback: string;
  success_rate: number;
  status: 'planned' | 'ongoing' | 'completed' | 'cancelled';
  created_at: string;
  updated_at: string;
}

interface MarketPrice {
  id: number;
  crop: number;
  district: number;
  market_name: string;
  price_per_kg: number;
  currency: string;
  quality_grade: 'A' | 'B' | 'C' | 'mixed';
  supply_level: 'low' | 'normal' | 'high' | 'oversupply';
  demand_level: 'low' | 'normal' | 'high';
  quantity_available_kg: number;
  price_trend: 'increasing' | 'stable' | 'decreasing';
  data_source: 'market_survey' | 'trader_report' | 'government' | 'cooperative' | 'online';
  date_recorded: string;
  created_at: string;
  updated_at: string;
}

interface Alert {
  id: number;
  title: string;
  description: string;
  alert_type: 'weather' | 'pest_disease' | 'market' | 'input_shortage' | 'extension' | 'policy' | 'emergency';
  severity: 'low' | 'medium' | 'high' | 'critical';
  districts: number[];
  sectors: number[];
  affected_crops: number[];
  target_cooperatives: number[];
  start_date: string;
  end_date: string;
  is_active: boolean;
  recommended_actions: string;
  resources_available: string;
  contact_person: string;
  contact_phone: string;
  farmers_reached: number;
  cooperatives_notified: number;
  actions_taken: string;
  effectiveness_score: number;
  created_at: string;
  updated_at: string;
}

interface Target {
  id: number;
  district: number;
  sector: number;
  crop: number;
  season: number;
  target_area_hectares: number;
  target_production_tons: number;
  target_yield_tons_per_hectare: number;
  target_farmers: number;
  allocated_budget: number;
  budget_for_seeds: number;
  budget_for_fertilizers: number;
  budget_for_extension: number;
  achieved_area_hectares: number;
  achieved_production_tons: number;
  farmers_participating: number;
  budget_utilized: number;
  created_at: string;
  updated_at: string;
}

interface Overview {
  total_farmers: number;
  total_cooperatives: number;
  total_crops: number;
  total_production: number;
  total_area: number;
  average_yield: number;
  market_prices: MarketPrice[];
  recent_alerts: Alert[];
  upcoming_extensions: Extension[];
  season_performance: {
    season: Season;
    achievement_rate: number;
  }[];
}

// Alerts
export const getAgricultureAlerts = () => api.get<Alert[]>('/agriculture/alerts/').then(r => r.data);
export const createAgricultureAlert = (data: Partial<Alert>) => api.post<Alert>('/agriculture/alerts/', data).then(r => r.data);
export const getAgricultureAlert = (id: number) => api.get<Alert>(`/agriculture/alerts/${id}/`).then(r => r.data);
export const updateAgricultureAlert = (id: number, data: Partial<Alert>) => api.put<Alert>(`/agriculture/alerts/${id}/`, data).then(r => r.data);
export const patchAgricultureAlert = (id: number, data: Partial<Alert>) => api.patch<Alert>(`/agriculture/alerts/${id}/`, data).then(r => r.data);
export const deleteAgricultureAlert = (id: number) => api.delete(`/agriculture/alerts/${id}/`).then(r => r.data);

// Cooperatives
export const getCooperatives = () => api.get<Cooperative[]>('/agriculture/cooperatives/').then(r => r.data);
export const createCooperative = (data: Partial<Cooperative>) => api.post<Cooperative>('/agriculture/cooperatives/', data).then(r => r.data);
export const getCooperative = (id: number) => api.get<Cooperative>(`/agriculture/cooperatives/${id}/`).then(r => r.data);
export const updateCooperative = (id: number, data: Partial<Cooperative>) => api.put<Cooperative>(`/agriculture/cooperatives/${id}/`, data).then(r => r.data);
export const patchCooperative = (id: number, data: Partial<Cooperative>) => api.patch<Cooperative>(`/agriculture/cooperatives/${id}/`, data).then(r => r.data);
export const deleteCooperative = (id: number) => api.delete(`/agriculture/cooperatives/${id}/`).then(r => r.data);
export const getCooperativePerformance = (id: number) => api.get<{ performance: number; details: any }>(`/agriculture/cooperatives/${id}/performance/`).then(r => r.data);

// Crops
export const getCrops = () => api.get<Crop[]>('/agriculture/crops/').then(r => r.data);
export const createCrop = (data: Partial<Crop>) => api.post<Crop>('/agriculture/crops/', data).then(r => r.data);
export const getCrop = (id: number) => api.get<Crop>(`/agriculture/crops/${id}/`).then(r => r.data);
export const updateCrop = (id: number, data: Partial<Crop>) => api.put<Crop>(`/agriculture/crops/${id}/`, data).then(r => r.data);
export const patchCrop = (id: number, data: Partial<Crop>) => api.patch<Crop>(`/agriculture/crops/${id}/`, data).then(r => r.data);
export const deleteCrop = (id: number) => api.delete(`/agriculture/crops/${id}/`).then(r => r.data);
export const getCropProductionStats = (id: number) => api.get<{ stats: any }>(`/agriculture/crops/${id}/production_stats/`).then(r => r.data);

// Farmers
export const getFarmers = () => api.get<Farmer[]>('/agriculture/farmers/').then(r => r.data);
export const createFarmer = (data: Partial<Farmer>) => api.post<Farmer>('/agriculture/farmers/', data).then(r => r.data);
export const getFarmer = (id: number) => api.get<Farmer>(`/agriculture/farmers/${id}/`).then(r => r.data);
export const updateFarmer = (id: number, data: Partial<Farmer>) => api.put<Farmer>(`/agriculture/farmers/${id}/`, data).then(r => r.data);
export const patchFarmer = (id: number, data: Partial<Farmer>) => api.patch<Farmer>(`/agriculture/farmers/${id}/`, data).then(r => r.data);
export const deleteFarmer = (id: number) => api.delete(`/agriculture/farmers/${id}/`).then(r => r.data);
export const getFarmerProductionHistory = (id: number) => api.get<Production[]>(`/agriculture/farmers/${id}/production_history/`).then(r => r.data);
export const getFarmerStats = (id: number) => api.get<{ stats: any }>(`/agriculture/farmers/${id}/stats/`).then(r => r.data);

// Extensions
export const getExtensions = () => api.get<Extension[]>('/agriculture/extensions/').then(r => r.data);
export const createExtension = (data: Partial<Extension>) => api.post<Extension>('/agriculture/extensions/', data).then(r => r.data);
export const getExtension = (id: number) => api.get<Extension>(`/agriculture/extensions/${id}/`).then(r => r.data);
export const updateExtension = (id: number, data: Partial<Extension>) => api.put<Extension>(`/agriculture/extensions/${id}/`, data).then(r => r.data);
export const patchExtension = (id: number, data: Partial<Extension>) => api.patch<Extension>(`/agriculture/extensions/${id}/`, data).then(r => r.data);
export const deleteExtension = (id: number) => api.delete(`/agriculture/extensions/${id}/`).then(r => r.data);

// Market Prices
export const getMarketPrices = () => api.get<MarketPrice[]>('/agriculture/market-prices/').then(r => r.data);
export const createMarketPrice = (data: Partial<MarketPrice>) => api.post<MarketPrice>('/agriculture/market-prices/', data).then(r => r.data);
export const getMarketPrice = (id: number) => api.get<MarketPrice>(`/agriculture/market-prices/${id}/`).then(r => r.data);
export const updateMarketPrice = (id: number, data: Partial<MarketPrice>) => api.put<MarketPrice>(`/agriculture/market-prices/${id}/`, data).then(r => r.data);
export const patchMarketPrice = (id: number, data: Partial<MarketPrice>) => api.patch<MarketPrice>(`/agriculture/market-prices/${id}/`, data).then(r => r.data);
export const deleteMarketPrice = (id: number) => api.delete(`/agriculture/market-prices/${id}/`).then(r => r.data);
export const getMarketPriceTrends = () => api.get<{ trends: any }>('/agriculture/market-prices/trends/').then(r => r.data);

// Productions
export const getProductions = () => api.get<Production[]>('/agriculture/productions/').then(r => r.data);
export const createProduction = (data: Partial<Production>) => api.post<Production>('/agriculture/productions/', data).then(r => r.data);
export const getProduction = (id: number) => api.get<Production>(`/agriculture/productions/${id}/`).then(r => r.data);
export const updateProduction = (id: number, data: Partial<Production>) => api.put<Production>(`/agriculture/productions/${id}/`, data).then(r => r.data);
export const patchProduction = (id: number, data: Partial<Production>) => api.patch<Production>(`/agriculture/productions/${id}/`, data).then(r => r.data);
export const deleteProduction = (id: number) => api.delete(`/agriculture/productions/${id}/`).then(r => r.data);
export const getProductionsAnalytics = () => api.get<{ analytics: any }>('/agriculture/productions/analytics/').then(r => r.data);

// Seasons
export const getSeasons = () => api.get<Season[]>('/agriculture/seasons/').then(r => r.data);
export const createSeason = (data: Partial<Season>) => api.post<Season>('/agriculture/seasons/', data).then(r => r.data);
export const getSeason = (id: number) => api.get<Season>(`/agriculture/seasons/${id}/`).then(r => r.data);
export const updateSeason = (id: number, data: Partial<Season>) => api.put<Season>(`/agriculture/seasons/${id}/`, data).then(r => r.data);
export const patchSeason = (id: number, data: Partial<Season>) => api.patch<Season>(`/agriculture/seasons/${id}/`, data).then(r => r.data);
export const deleteSeason = (id: number) => api.delete(`/agriculture/seasons/${id}/`).then(r => r.data);
export const getSeasonPerformance = (id: number) => api.get<{ performance: any }>(`/agriculture/seasons/${id}/performance/`).then(r => r.data);

// Targets
export const getTargets = () => api.get<Target[]>('/agriculture/targets/').then(r => r.data);
export const createTarget = (data: Partial<Target>) => api.post<Target>('/agriculture/targets/', data).then(r => r.data);
export const getTarget = (id: number) => api.get<Target>(`/agriculture/targets/${id}/`).then(r => r.data);
export const updateTarget = (id: number, data: Partial<Target>) => api.put<Target>(`/agriculture/targets/${id}/`, data).then(r => r.data);
export const patchTarget = (id: number, data: Partial<Target>) => api.patch<Target>(`/agriculture/targets/${id}/`, data).then(r => r.data);
export const deleteTarget = (id: number) => api.delete(`/agriculture/targets/${id}/`).then(r => r.data);

// Overview
export const getAgricultureOverview = () => api.get<Overview>('/agriculture/dashboard/overview/').then(r => r.data); 