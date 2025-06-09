import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

// Alerts
export const getAgricultureAlerts = () => api.get('/agriculture/alerts/').then(r => r.data);
export const createAgricultureAlert = (data) => api.post('/agriculture/alerts/', data).then(r => r.data);
export const getAgricultureAlert = (id) => api.get(`/agriculture/alerts/${id}/`).then(r => r.data);
export const updateAgricultureAlert = (id, data) => api.put(`/agriculture/alerts/${id}/`, data).then(r => r.data);
export const patchAgricultureAlert = (id, data) => api.patch(`/agriculture/alerts/${id}/`, data).then(r => r.data);
export const deleteAgricultureAlert = (id) => api.delete(`/agriculture/alerts/${id}/`).then(r => r.data);

// Cooperatives
export const getCooperatives = () => api.get('/agriculture/cooperatives/').then(r => r.data);
export const createCooperative = (data) => api.post('/agriculture/cooperatives/', data).then(r => r.data);
export const getCooperative = (id) => api.get(`/agriculture/cooperatives/${id}/`).then(r => r.data);
export const updateCooperative = (id, data) => api.put(`/agriculture/cooperatives/${id}/`, data).then(r => r.data);
export const patchCooperative = (id, data) => api.patch(`/agriculture/cooperatives/${id}/`, data).then(r => r.data);
export const deleteCooperative = (id) => api.delete(`/agriculture/cooperatives/${id}/`).then(r => r.data);
export const getCooperativePerformance = (id) => api.get(`/agriculture/cooperatives/${id}/performance/`).then(r => r.data);

// Crops
export const getCrops = () => api.get('/agriculture/crops/').then(r => r.data);
export const createCrop = (data) => api.post('/agriculture/crops/', data).then(r => r.data);
export const getCrop = (id) => api.get(`/agriculture/crops/${id}/`).then(r => r.data);
export const updateCrop = (id, data) => api.put(`/agriculture/crops/${id}/`, data).then(r => r.data);
export const patchCrop = (id, data) => api.patch(`/agriculture/crops/${id}/`, data).then(r => r.data);
export const deleteCrop = (id) => api.delete(`/agriculture/crops/${id}/`).then(r => r.data);
export const getCropProductionStats = (id) => api.get(`/agriculture/crops/${id}/production_stats/`).then(r => r.data);

// Farmers
export const getFarmers = () => api.get('/agriculture/farmers/').then(r => r.data);
export const createFarmer = (data) => api.post('/agriculture/farmers/', data).then(r => r.data);
export const getFarmer = (id) => api.get(`/agriculture/farmers/${id}/`).then(r => r.data);
export const updateFarmer = (id, data) => api.put(`/agriculture/farmers/${id}/`, data).then(r => r.data);
export const patchFarmer = (id, data) => api.patch(`/agriculture/farmers/${id}/`, data).then(r => r.data);
export const deleteFarmer = (id) => api.delete(`/agriculture/farmers/${id}/`).then(r => r.data);
export const getFarmerProductionHistory = (id) => api.get(`/agriculture/farmers/${id}/production_history/`).then(r => r.data);
export const getFarmerStats = (id) => api.get(`/agriculture/farmers/${id}/stats/`).then(r => r.data);

// Extensions
export const getExtensions = () => api.get('/agriculture/extensions/').then(r => r.data);
export const createExtension = (data) => api.post('/agriculture/extensions/', data).then(r => r.data);
export const getExtension = (id) => api.get(`/agriculture/extensions/${id}/`).then(r => r.data);
export const updateExtension = (id, data) => api.put(`/agriculture/extensions/${id}/`, data).then(r => r.data);
export const patchExtension = (id, data) => api.patch(`/agriculture/extensions/${id}/`, data).then(r => r.data);
export const deleteExtension = (id) => api.delete(`/agriculture/extensions/${id}/`).then(r => r.data);

// Market Prices
export const getMarketPrices = () => api.get('/agriculture/market-prices/').then(r => r.data);
export const createMarketPrice = (data) => api.post('/agriculture/market-prices/', data).then(r => r.data);
export const getMarketPrice = (id) => api.get(`/agriculture/market-prices/${id}/`).then(r => r.data);
export const updateMarketPrice = (id, data) => api.put(`/agriculture/market-prices/${id}/`, data).then(r => r.data);
export const patchMarketPrice = (id, data) => api.patch(`/agriculture/market-prices/${id}/`, data).then(r => r.data);
export const deleteMarketPrice = (id) => api.delete(`/agriculture/market-prices/${id}/`).then(r => r.data);
export const getMarketPriceTrends = () => api.get('/agriculture/market-prices/trends/').then(r => r.data);

// Productions
export const getProductions = () => api.get('/agriculture/productions/').then(r => r.data);
export const createProduction = (data) => api.post('/agriculture/productions/', data).then(r => r.data);
export const getProduction = (id) => api.get(`/agriculture/productions/${id}/`).then(r => r.data);
export const updateProduction = (id, data) => api.put(`/agriculture/productions/${id}/`, data).then(r => r.data);
export const patchProduction = (id, data) => api.patch(`/agriculture/productions/${id}/`, data).then(r => r.data);
export const deleteProduction = (id) => api.delete(`/agriculture/productions/${id}/`).then(r => r.data);
export const getProductionsAnalytics = () => api.get('/agriculture/productions/analytics/').then(r => r.data);

// Seasons
export const getSeasons = () => api.get('/agriculture/seasons/').then(r => r.data);
export const createSeason = (data) => api.post('/agriculture/seasons/', data).then(r => r.data);
export const getSeason = (id) => api.get(`/agriculture/seasons/${id}/`).then(r => r.data);
export const updateSeason = (id, data) => api.put(`/agriculture/seasons/${id}/`, data).then(r => r.data);
export const patchSeason = (id, data) => api.patch(`/agriculture/seasons/${id}/`, data).then(r => r.data);
export const deleteSeason = (id) => api.delete(`/agriculture/seasons/${id}/`).then(r => r.data);
export const getSeasonPerformance = (id) => api.get(`/agriculture/seasons/${id}/performance/`).then(r => r.data);

// Targets
export const getTargets = () => api.get('/agriculture/targets/').then(r => r.data);
export const createTarget = (data) => api.post('/agriculture/targets/', data).then(r => r.data);
export const getTarget = (id) => api.get(`/agriculture/targets/${id}/`).then(r => r.data);
export const updateTarget = (id, data) => api.put(`/agriculture/targets/${id}/`, data).then(r => r.data);
export const patchTarget = (id, data) => api.patch(`/agriculture/targets/${id}/`, data).then(r => r.data);
export const deleteTarget = (id) => api.delete(`/agriculture/targets/${id}/`).then(r => r.data);

// Overview
export const getAgricultureOverview = () => api.get('/agriculture/dashboard/overview/').then(r => r.data); 