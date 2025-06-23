import { useToast as useVueToast } from 'vue-toastification'

export function useToast() {
  const toast = useVueToast()

  const showSuccess = (message: string, title?: string) => {
    toast.success(title ? `${title}: ${message}` : message, {
      timeout: 3000,
      icon: '✅'
    })
  }

  const showError = (message: string, title?: string) => {
    toast.error(title ? `${title}: ${message}` : message, {
      timeout: 5000,
      icon: '❌'
    })
  }

  const showWarning = (message: string, title?: string) => {
    toast.warning(title ? `${title}: ${message}` : message, {
      timeout: 4000,
      icon: '⚠️'
    })
  }

  const showInfo = (message: string, title?: string) => {
    toast.info(title ? `${title}: ${message}` : message, {
      timeout: 3000,
      icon: 'ℹ️'
    })
  }

  const showLoading = (message: string) => {
    return toast.info(message, {
      timeout: false,
      closeOnClick: false,
      closeButton: false,
      icon: '⏳'
    })
  }

  const dismiss = (toastId: any) => {
    toast.dismiss(toastId)
  }

  const clear = () => {
    toast.clear()
  }

  return {
    showSuccess,
    showError,
    showWarning,
    showInfo,
    showLoading,
    dismiss,
    clear
  }
}
