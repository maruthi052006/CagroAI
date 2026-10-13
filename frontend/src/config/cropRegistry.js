// Crop Registry Config - 40 Crops
export const cropRegistry = [
    // --- GrassStalkArchetype (8) ---
    { id: "rice", displayName: "Rice", archetype: "GrassStalkArchetype", matureHeight: 0.9, stalkColor: "#8fb562", headColor: "#d9d082", density: "high", icon: "wheat" },
    { id: "wheat", displayName: "Wheat", archetype: "GrassStalkArchetype", matureHeight: 1.0, stalkColor: "#c2b87a", headColor: "#e0d08b", density: "high", icon: "wheat" },
    { id: "maize", displayName: "Maize (Corn)", archetype: "GrassStalkArchetype", matureHeight: 1.8, stalkColor: "#7a9b45", headColor: "#edd766", density: "medium", icon: "wheat" },
    { id: "barley", displayName: "Barley", archetype: "GrassStalkArchetype", matureHeight: 0.8, stalkColor: "#aebf7e", headColor: "#e6d7a1", density: "high", icon: "wheat" },
    { id: "sorghum", displayName: "Sorghum", archetype: "GrassStalkArchetype", matureHeight: 1.6, stalkColor: "#759942", headColor: "#a35029", density: "medium", icon: "wheat" },
    { id: "pearl_millet", displayName: "Pearl Millet", archetype: "GrassStalkArchetype", matureHeight: 1.5, stalkColor: "#8da366", headColor: "#b3aa8a", density: "medium", icon: "wheat" },
    { id: "finger_millet", displayName: "Finger Millet", archetype: "GrassStalkArchetype", matureHeight: 0.7, stalkColor: "#748f4b", headColor: "#9c6b4d", density: "high", icon: "wheat" },
    { id: "sugarcane", displayName: "Sugarcane", archetype: "GrassStalkArchetype", matureHeight: 2.2, stalkColor: "#b5c777", headColor: "#d4d4d4", density: "medium", icon: "align-justify" },

    // --- BulbArchetype (4) ---
    { id: "onion", displayName: "Onion", archetype: "BulbArchetype", matureHeight: 0.4, stalkColor: "#4D7C3A", headColor: "#E8C87A", density: "high", icon: "leaf" },
    { id: "garlic", displayName: "Garlic", archetype: "BulbArchetype", matureHeight: 0.35, stalkColor: "#578c43", headColor: "#f2f0e6", density: "high", icon: "leaf" },
    { id: "turmeric", displayName: "Turmeric", archetype: "BulbArchetype", matureHeight: 0.6, stalkColor: "#679e49", headColor: "#de8221", density: "medium", icon: "leaf" },
    { id: "ginger", displayName: "Ginger", archetype: "BulbArchetype", matureHeight: 0.5, stalkColor: "#609c48", headColor: "#c2a66f", density: "medium", icon: "leaf" },

    // --- RootLeafArchetype (4) ---
    { id: "carrot", displayName: "Carrot", archetype: "RootLeafArchetype", matureHeight: 0.3, leafColor: "#498f39", headColor: "#e87c17", density: "high", icon: "leaf" },
    { id: "radish", displayName: "Radish", archetype: "RootLeafArchetype", matureHeight: 0.25, leafColor: "#509e3f", headColor: "#e81744", density: "high", icon: "leaf" },
    { id: "beetroot", displayName: "Beetroot", archetype: "RootLeafArchetype", matureHeight: 0.25, leafColor: "#613b45", headColor: "#7d1632", density: "medium", icon: "leaf" },
    { id: "potato", displayName: "Potato", archetype: "RootLeafArchetype", matureHeight: 0.4, leafColor: "#538a41", headColor: "#c4ab7a", density: "medium", icon: "leaf" },

    // --- FlowerHeadArchetype (2) ---
    { id: "sunflower", displayName: "Sunflower", archetype: "FlowerHeadArchetype", matureHeight: 1.5, stalkColor: "#4f8a37", headColor: "#f2d31b", density: "low", icon: "sun" },
    { id: "mustard", displayName: "Mustard", archetype: "FlowerHeadArchetype", matureHeight: 0.8, stalkColor: "#60a145", headColor: "#f0df24", density: "high", icon: "sun" },

    // --- BushFruitArchetype (6) ---
    { id: "tomato", displayName: "Tomato", archetype: "BushFruitArchetype", matureHeight: 0.8, stalkColor: "#4f753c", leafColor: "#40692d", headColor: "#e62727", density: "medium", icon: "cherry" },
    { id: "chili", displayName: "Chili/Pepper", archetype: "BushFruitArchetype", matureHeight: 0.6, stalkColor: "#517540", leafColor: "#476e33", headColor: "#c21111", density: "medium", icon: "cherry" },
    { id: "brinjal", displayName: "Brinjal", archetype: "BushFruitArchetype", matureHeight: 0.7, stalkColor: "#664366", leafColor: "#577a41", headColor: "#5e1d5e", density: "medium", icon: "cherry" },
    { id: "okra", displayName: "Okra", archetype: "BushFruitArchetype", matureHeight: 0.9, stalkColor: "#527d42", leafColor: "#4b753a", headColor: "#8db57a", density: "medium", icon: "cherry" },
    { id: "cotton", displayName: "Cotton", archetype: "BushFruitArchetype", matureHeight: 1.0, stalkColor: "#7a6358", leafColor: "#5e754a", headColor: "#ffffff", density: "medium", icon: "cloud" },
    { id: "tea", displayName: "Tea", archetype: "BushFruitArchetype", matureHeight: 1.2, stalkColor: "#594d46", leafColor: "#335e26", headColor: "#335e26", density: "low", icon: "coffee" },

    // --- LegumeBushArchetype (7) ---
    { id: "groundnut", displayName: "Groundnut", archetype: "LegumeBushArchetype", matureHeight: 0.4, stalkColor: "#608048", leafColor: "#5b873e", headColor: "#b5a278", density: "high", icon: "bean" },
    { id: "soybean", displayName: "Soybean", archetype: "LegumeBushArchetype", matureHeight: 0.6, stalkColor: "#698a4a", leafColor: "#58783d", headColor: "#d9d082", density: "medium", icon: "bean" },
    { id: "chickpea", displayName: "Chickpea", archetype: "LegumeBushArchetype", matureHeight: 0.5, stalkColor: "#5b873e", leafColor: "#4c7331", headColor: "#9e916a", density: "medium", icon: "bean" },
    { id: "lentil", displayName: "Lentil", archetype: "LegumeBushArchetype", matureHeight: 0.4, stalkColor: "#66854b", leafColor: "#5a7a3e", headColor: "#85623e", density: "high", icon: "bean" },
    { id: "pigeon_pea", displayName: "Pigeon Pea", archetype: "LegumeBushArchetype", matureHeight: 1.1, stalkColor: "#577341", leafColor: "#4e693a", headColor: "#736b41", density: "medium", icon: "bean" },
    { id: "green_gram", displayName: "Green Gram", archetype: "LegumeBushArchetype", matureHeight: 0.5, stalkColor: "#5d8041", leafColor: "#597840", headColor: "#35591c", density: "high", icon: "bean" },
    { id: "black_gram", displayName: "Black Gram", archetype: "LegumeBushArchetype", matureHeight: 0.5, stalkColor: "#5a7841", leafColor: "#506e39", headColor: "#2a2e26", density: "high", icon: "bean" },

    // --- VineArchetype (6) ---
    { id: "cucumber", displayName: "Cucumber", archetype: "VineArchetype", matureHeight: 1.2, leafColor: "#457530", headColor: "#508535", density: "medium", icon: "grape" },
    { id: "bottle_gourd", displayName: "Bottle Gourd", archetype: "VineArchetype", matureHeight: 1.5, leafColor: "#56873e", headColor: "#9cbd84", density: "low", icon: "grape" },
    { id: "bitter_gourd", displayName: "Bitter Gourd", archetype: "VineArchetype", matureHeight: 1.4, leafColor: "#4a7834", headColor: "#3b6327", density: "low", icon: "grape" },
    { id: "pumpkin", displayName: "Pumpkin", archetype: "VineArchetype", matureHeight: 0.3, leafColor: "#487334", headColor: "#d98c25", density: "low", icon: "grape" },
    { id: "watermelon", displayName: "Watermelon", archetype: "VineArchetype", matureHeight: 0.3, leafColor: "#477035", headColor: "#295719", density: "low", icon: "grape" },
    { id: "grape", displayName: "Grape", archetype: "VineArchetype", matureHeight: 2.0, leafColor: "#53873c", headColor: "#603673", density: "medium", icon: "grape" },

    // --- PseudostemArchetype (1) ---
    { id: "banana", displayName: "Banana", archetype: "PseudostemArchetype", matureHeight: 2.5, stalkColor: "#496336", leafColor: "#587d3d", headColor: "#ebd95b", density: "low", icon: "trees" },

    // --- FiberStalkArchetype (2) ---
    { id: "jute", displayName: "Jute", archetype: "FiberStalkArchetype", matureHeight: 2.2, stalkColor: "#759c54", leafColor: "#56753d", density: "high", icon: "align-center" },
    { id: "sesame", displayName: "Sesame", archetype: "FiberStalkArchetype", matureHeight: 1.2, stalkColor: "#678a48", leafColor: "#486330", density: "high", icon: "align-center" }
];
