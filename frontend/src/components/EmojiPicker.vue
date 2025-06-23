<template>
  <div class="emoji-picker" v-if="isVisible">
    <div class="emoji-picker-header">
      <div class="emoji-categories">
        <button
          v-for="category in categories"
          :key="category.name"
          @click="selectedCategory = category.name"
          :class="{ active: selectedCategory === category.name }"
          class="category-btn"
        >
          {{ category.icon }}
        </button>
      </div>
      <button @click="$emit('close')" class="close-btn">×</button>
    </div>

    <div class="emoji-search">
      <input
        v-model="searchQuery"
        placeholder="Search emojis..."
        class="search-input"
      />
    </div>

    <div class="emoji-grid">
      <button
        v-for="emoji in filteredEmojis"
        :key="emoji.emoji"
        @click="selectEmoji(emoji)"
        class="emoji-btn"
        :title="emoji.name"
      >
        {{ emoji.emoji }}
      </button>
    </div>

    <div class="recent-emojis" v-if="recentEmojis.length">
      <h4>Recently Used</h4>
      <div class="emoji-row">
        <button
          v-for="emoji in recentEmojis"
          :key="emoji.emoji"
          @click="selectEmoji(emoji)"
          class="emoji-btn"
          :title="emoji.name"
        >
          {{ emoji.emoji }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select', 'close'])

const searchQuery = ref('')
const selectedCategory = ref('smileys')
const recentEmojis = ref([])

// Emoji categories and data
const categories = [
  { name: 'smileys', icon: '😀' },
  { name: 'people', icon: '👤' },
  { name: 'nature', icon: '🌿' },
  { name: 'food', icon: '🍎' },
  { name: 'activities', icon: '⚽' },
  { name: 'symbols', icon: '❤️' }
]

const emojiData = {
  smileys: [
    { emoji: '😀', name: 'grinning_face' },
    { emoji: '😃', name: 'grinning_face_with_big_eyes' },
    { emoji: '😄', name: 'grinning_face_with_smiling_eyes' },
    { emoji: '😁', name: 'beaming_face_with_smiling_eyes' },
    { emoji: '😆', name: 'grinning_squinting_face' },
    { emoji: '😅', name: 'grinning_face_with_sweat' },
    { emoji: '🤣', name: 'rolling_on_the_floor_laughing' },
    { emoji: '😂', name: 'face_with_tears_of_joy' },
    { emoji: '🙂', name: 'slightly_smiling_face' },
    { emoji: '🙃', name: 'upside_down_face' },
    { emoji: '😉', name: 'winking_face' },
    { emoji: '😊', name: 'smiling_face_with_smiling_eyes' },
    { emoji: '😇', name: 'smiling_face_with_halo' },
    { emoji: '🥰', name: 'smiling_face_with_hearts' },
    { emoji: '😍', name: 'smiling_face_with_heart_eyes' },
    { emoji: '🤩', name: 'star_struck' },
    { emoji: '😘', name: 'face_blowing_a_kiss' },
    { emoji: '😗', name: 'kissing_face' },
    { emoji: '😚', name: 'kissing_face_with_closed_eyes' },
    { emoji: '😙', name: 'kissing_face_with_smiling_eyes' },
    { emoji: '😋', name: 'face_savoring_food' },
    { emoji: '😛', name: 'face_with_tongue' },
    { emoji: '😜', name: 'winking_face_with_tongue' },
    { emoji: '🤪', name: 'zany_face' },
    { emoji: '😝', name: 'squinting_face_with_tongue' },
    { emoji: '🤑', name: 'money_mouth_face' },
    { emoji: '🤗', name: 'hugging_face' },
    { emoji: '🤭', name: 'face_with_hand_over_mouth' },
    { emoji: '🤫', name: 'shushing_face' },
    { emoji: '🤔', name: 'thinking_face' },
    { emoji: '🤐', name: 'zipper_mouth_face' },
    { emoji: '🤨', name: 'face_with_raised_eyebrow' },
    { emoji: '😐', name: 'neutral_face' },
    { emoji: '😑', name: 'expressionless_face' },
    { emoji: '😶', name: 'face_without_mouth' },
    { emoji: '😏', name: 'smirking_face' },
    { emoji: '😒', name: 'unamused_face' },
    { emoji: '🙄', name: 'face_with_rolling_eyes' },
    { emoji: '😬', name: 'grimacing_face' },
    { emoji: '🤥', name: 'lying_face' },
    { emoji: '😔', name: 'pensive_face' },
    { emoji: '😪', name: 'sleepy_face' },
    { emoji: '🤤', name: 'drooling_face' },
    { emoji: '😴', name: 'sleeping_face' },
    { emoji: '😷', name: 'face_with_medical_mask' },
    { emoji: '🤒', name: 'face_with_thermometer' },
    { emoji: '🤕', name: 'face_with_head_bandage' },
    { emoji: '🤢', name: 'nauseated_face' },
    { emoji: '🤮', name: 'face_vomiting' },
    { emoji: '🤧', name: 'sneezing_face' },
    { emoji: '🥵', name: 'hot_face' },
    { emoji: '🥶', name: 'cold_face' },
    { emoji: '🥴', name: 'woozy_face' },
    { emoji: '😵', name: 'dizzy_face' },
    { emoji: '🤯', name: 'exploding_head' },
    { emoji: '🤠', name: 'cowboy_hat_face' },
    { emoji: '🥳', name: 'partying_face' },
    { emoji: '😎', name: 'smiling_face_with_sunglasses' },
    { emoji: '🤓', name: 'nerd_face' },
    { emoji: '🧐', name: 'face_with_monocle' }
  ],
  people: [
    { emoji: '👍', name: 'thumbs_up' },
    { emoji: '👎', name: 'thumbs_down' },
    { emoji: '👌', name: 'ok_hand' },
    { emoji: '✌️', name: 'victory_hand' },
    { emoji: '🤞', name: 'crossed_fingers' },
    { emoji: '🤟', name: 'love_you_gesture' },
    { emoji: '🤘', name: 'sign_of_the_horns' },
    { emoji: '🤙', name: 'call_me_hand' },
    { emoji: '👈', name: 'backhand_index_pointing_left' },
    { emoji: '👉', name: 'backhand_index_pointing_right' },
    { emoji: '👆', name: 'backhand_index_pointing_up' },
    { emoji: '👇', name: 'backhand_index_pointing_down' },
    { emoji: '☝️', name: 'index_pointing_up' },
    { emoji: '✋', name: 'raised_hand' },
    { emoji: '🤚', name: 'raised_back_of_hand' },
    { emoji: '🖐️', name: 'hand_with_fingers_splayed' },
    { emoji: '🖖', name: 'vulcan_salute' },
    { emoji: '👋', name: 'waving_hand' },
    { emoji: '🤝', name: 'handshake' },
    { emoji: '👏', name: 'clapping_hands' },
    { emoji: '🙌', name: 'raising_hands' },
    { emoji: '👐', name: 'open_hands' },
    { emoji: '🤲', name: 'palms_up_together' },
    { emoji: '🤜', name: 'right_facing_fist' },
    { emoji: '🤛', name: 'left_facing_fist' },
    { emoji: '✊', name: 'raised_fist' },
    { emoji: '👊', name: 'oncoming_fist' },
    { emoji: '🙏', name: 'folded_hands' }
  ],
  nature: [
    { emoji: '🌱', name: 'seedling' },
    { emoji: '🌿', name: 'herb' },
    { emoji: '🍀', name: 'four_leaf_clover' },
    { emoji: '🌾', name: 'sheaf_of_rice' },
    { emoji: '🌵', name: 'cactus' },
    { emoji: '🌲', name: 'evergreen_tree' },
    { emoji: '🌳', name: 'deciduous_tree' },
    { emoji: '🌴', name: 'palm_tree' },
    { emoji: '🌸', name: 'cherry_blossom' },
    { emoji: '🌺', name: 'hibiscus' },
    { emoji: '🌻', name: 'sunflower' },
    { emoji: '🌹', name: 'rose' },
    { emoji: '🌷', name: 'tulip' },
    { emoji: '🌼', name: 'blossom' },
    { emoji: '💐', name: 'bouquet' },
    { emoji: '🍄', name: 'mushroom' },
    { emoji: '🌰', name: 'chestnut' },
    { emoji: '🐶', name: 'dog_face' },
    { emoji: '🐱', name: 'cat_face' },
    { emoji: '🐭', name: 'mouse_face' },
    { emoji: '🐹', name: 'hamster_face' },
    { emoji: '🐰', name: 'rabbit_face' },
    { emoji: '🦊', name: 'fox_face' },
    { emoji: '🐻', name: 'bear_face' },
    { emoji: '🐼', name: 'panda_face' },
    { emoji: '🐨', name: 'koala' },
    { emoji: '🐯', name: 'tiger_face' },
    { emoji: '🦁', name: 'lion_face' },
    { emoji: '🐮', name: 'cow_face' },
    { emoji: '🐷', name: 'pig_face' },
    { emoji: '🐸', name: 'frog_face' },
    { emoji: '🐵', name: 'monkey_face' }
  ],
  food: [
    { emoji: '🍎', name: 'red_apple' },
    { emoji: '🍊', name: 'tangerine' },
    { emoji: '🍋', name: 'lemon' },
    { emoji: '🍌', name: 'banana' },
    { emoji: '🍉', name: 'watermelon' },
    { emoji: '🍇', name: 'grapes' },
    { emoji: '🍓', name: 'strawberry' },
    { emoji: '🍈', name: 'melon' },
    { emoji: '🍒', name: 'cherries' },
    { emoji: '🍑', name: 'peach' },
    { emoji: '🥭', name: 'mango' },
    { emoji: '🍍', name: 'pineapple' },
    { emoji: '🥥', name: 'coconut' },
    { emoji: '🥝', name: 'kiwi_fruit' },
    { emoji: '🍅', name: 'tomato' },
    { emoji: '🍆', name: 'eggplant' },
    { emoji: '🥑', name: 'avocado' },
    { emoji: '🥦', name: 'broccoli' },
    { emoji: '🥬', name: 'leafy_greens' },
    { emoji: '🥒', name: 'cucumber' },
    { emoji: '🌶️', name: 'hot_pepper' },
    { emoji: '🌽', name: 'ear_of_corn' },
    { emoji: '🥕', name: 'carrot' },
    { emoji: '🧄', name: 'garlic' },
    { emoji: '🧅', name: 'onion' },
    { emoji: '🥔', name: 'potato' },
    { emoji: '🍠', name: 'roasted_sweet_potato' },
    { emoji: '🥐', name: 'croissant' },
    { emoji: '🥖', name: 'baguette_bread' },
    { emoji: '🍞', name: 'bread' },
    { emoji: '🥨', name: 'pretzel' },
    { emoji: '🥯', name: 'bagel' }
  ],
  activities: [
    { emoji: '⚽', name: 'soccer_ball' },
    { emoji: '🏀', name: 'basketball' },
    { emoji: '🏈', name: 'american_football' },
    { emoji: '⚾', name: 'baseball' },
    { emoji: '🥎', name: 'softball' },
    { emoji: '🎾', name: 'tennis' },
    { emoji: '🏐', name: 'volleyball' },
    { emoji: '🏉', name: 'rugby_football' },
    { emoji: '🥏', name: 'flying_disc' },
    { emoji: '🎱', name: 'pool_8_ball' },
    { emoji: '🪀', name: 'yo_yo' },
    { emoji: '🏓', name: 'ping_pong' },
    { emoji: '🏸', name: 'badminton' },
    { emoji: '🥅', name: 'goal_net' },
    { emoji: '⛳', name: 'flag_in_hole' },
    { emoji: '🪁', name: 'kite' },
    { emoji: '🏹', name: 'bow_and_arrow' },
    { emoji: '🎣', name: 'fishing_pole' },
    { emoji: '🤿', name: 'diving_mask' },
    { emoji: '🥊', name: 'boxing_glove' },
    { emoji: '🥋', name: 'martial_arts_uniform' },
    { emoji: '🎽', name: 'running_shirt' },
    { emoji: '🛹', name: 'skateboard' },
    { emoji: '🛷', name: 'sled' },
    { emoji: '⛸️', name: 'ice_skate' },
    { emoji: '🥌', name: 'curling_stone' },
    { emoji: '🎿', name: 'skis' },
    { emoji: '⛷️', name: 'skier' },
    { emoji: '🏂', name: 'snowboarder' },
    { emoji: '🪂', name: 'parachute' },
    { emoji: '🏋️', name: 'person_lifting_weights' },
    { emoji: '🤸', name: 'person_cartwheeling' }
  ],
  symbols: [
    { emoji: '❤️', name: 'red_heart' },
    { emoji: '🧡', name: 'orange_heart' },
    { emoji: '💛', name: 'yellow_heart' },
    { emoji: '💚', name: 'green_heart' },
    { emoji: '💙', name: 'blue_heart' },
    { emoji: '💜', name: 'purple_heart' },
    { emoji: '🖤', name: 'black_heart' },
    { emoji: '🤍', name: 'white_heart' },
    { emoji: '🤎', name: 'brown_heart' },
    { emoji: '💔', name: 'broken_heart' },
    { emoji: '❣️', name: 'heart_exclamation' },
    { emoji: '💕', name: 'two_hearts' },
    { emoji: '💞', name: 'revolving_hearts' },
    { emoji: '💓', name: 'beating_heart' },
    { emoji: '💗', name: 'growing_heart' },
    { emoji: '💖', name: 'sparkling_heart' },
    { emoji: '💘', name: 'heart_with_arrow' },
    { emoji: '💝', name: 'heart_with_ribbon' },
    { emoji: '💟', name: 'heart_decoration' },
    { emoji: '☮️', name: 'peace_symbol' },
    { emoji: '✝️', name: 'latin_cross' },
    { emoji: '☪️', name: 'star_and_crescent' },
    { emoji: '🕉️', name: 'om' },
    { emoji: '☸️', name: 'wheel_of_dharma' },
    { emoji: '✡️', name: 'star_of_david' },
    { emoji: '🔯', name: 'dotted_six_pointed_star' },
    { emoji: '🕎', name: 'menorah' },
    { emoji: '☯️', name: 'yin_yang' },
    { emoji: '☦️', name: 'orthodox_cross' },
    { emoji: '🛐', name: 'place_of_worship' },
    { emoji: '⛎', name: 'ophiuchus' },
    { emoji: '♈', name: 'aries' }
  ]
}

const filteredEmojis = computed(() => {
  let emojis = emojiData[selectedCategory.value] || []

  if (searchQuery.value) {
    emojis = Object.values(emojiData).flat().filter(emoji =>
      emoji.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      emoji.emoji.includes(searchQuery.value)
    )
  }

  return emojis
})

const selectEmoji = (emoji) => {
  // Add to recent emojis
  const existingIndex = recentEmojis.value.findIndex(e => e.emoji === emoji.emoji)
  if (existingIndex > -1) {
    recentEmojis.value.splice(existingIndex, 1)
  }
  recentEmojis.value.unshift(emoji)
  recentEmojis.value = recentEmojis.value.slice(0, 20) // Keep only 20 recent emojis

  // Save to localStorage
  localStorage.setItem('recentEmojis', JSON.stringify(recentEmojis.value))

  emit('select', emoji)
}

onMounted(() => {
  // Load recent emojis from localStorage
  const saved = localStorage.getItem('recentEmojis')
  if (saved) {
    recentEmojis.value = JSON.parse(saved)
  }
})
</script>

<style scoped>
.emoji-picker {
  position: absolute;
  bottom: 100%;
  right: 0;
  width: 320px;
  max-height: 400px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
}

.emoji-picker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.emoji-categories {
  display: flex;
  gap: 4px;
}

.category-btn {
  background: none;
  border: none;
  padding: 6px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.2s;
}

.category-btn:hover {
  background: #e9ecef;
}

.category-btn.active {
  background: #007bff;
  color: white;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}

.close-btn:hover {
  background: #e9ecef;
}

.emoji-search {
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.search-input {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 2px;
  padding: 8px;
  max-height: 200px;
  overflow-y: auto;
}

.emoji-btn {
  background: none;
  border: none;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 18px;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.emoji-btn:hover {
  background: #f8f9fa;
}

.recent-emojis {
  border-top: 1px solid #eee;
  padding: 8px;
}

.recent-emojis h4 {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
}

.emoji-row {
  display: flex;
  gap: 2px;
  flex-wrap: wrap;
}

.emoji-row .emoji-btn {
  font-size: 16px;
  padding: 6px;
}
</style>