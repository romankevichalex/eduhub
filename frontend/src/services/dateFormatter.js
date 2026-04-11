/**
 * Форматирует ISO-строку в локальное время пользователя
 * @param {string} isoString - дата в формате ISO (с Z или без)
 * @param {object} options
 * @param {boolean} options.showDate - добавить дату перед временем
 * @returns {string}
 */
export function formatMessageTime(isoString, { showDate = false } = {}) {
  if (!isoString) return ''
  
  // Нормализация: если нет Z и нет смещения, считаем что это UTC
  let normalized = isoString
  if (!isoString.includes('Z') && !isoString.includes('+') && !isoString.includes('-', 10)) {
    normalized = isoString + 'Z'
  }
  
  const date = new Date(normalized)
  
  // Получаем локаль и часовой пояс браузера
  const locale = navigator.language || 'ru-RU'
  const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone
  
  const timeOptions = {
    hour: '2-digit',
    minute: '2-digit',
    timeZone
  }
  
  const timeStr = date.toLocaleTimeString(locale, timeOptions)
  
  if (showDate) {
    const dateStr = date.toLocaleDateString(locale, { timeZone })
    return `${dateStr} ${timeStr}`
  }
  
  return timeStr
}