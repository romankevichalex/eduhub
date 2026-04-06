<template>
  <div class="top-bar">
    <div class="top-bar-title">Мои предметы</div>
    <div class="top-bar-subtitle">Кафедра интеллектуальных систем</div>
  </div>
  <div class="divider"></div>  <!-- разделитель между кнопками -->
</template>

<style scoped>
.top-bar {
  background: var(--gradient);
  padding: 20px 16px;
  border-bottom: 2px solid var(--gray-1); 
}
.top-bar-title {
  font-size: 24px;
  font-weight: 600;
  color: white;
}
.top-bar-subtitle {
  font-size: 14px;
  color: rgba(255,255,255,0.8);
  margin-top: 4px;
}
</style>