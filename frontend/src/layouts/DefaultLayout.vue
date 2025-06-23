<template>
  <div class="app-layout">
    <!-- Header Component -->
    <Header />
    
    <!-- Main Content Area -->
    <main class="main-content">
      <router-view />
    </main>
    
    <!-- Footer Component -->
    <Footer />
  </div>
</template>

<script>
import Header from '../components/header/Header.vue'
import Footer from '../components/footer/Footer.vue'

export default {
  name: 'DefaultLayout',
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 0;
  /* Add any global padding/margin for your content here */
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .main-content {
    padding: 0;
  }
}
</style>
