<template>
  <div class="call-interface">
    <!-- Call Controls -->
    <div class="call-controls">
      <button
        @click="initiateCall('audio')"
        class="call-btn audio-call"
        title="Start Audio Call"
        :disabled="isInCall"
      >
        📞
      </button>
      <button
        @click="initiateCall('video')"
        class="call-btn video-call"
        title="Start Video Call"
        :disabled="isInCall"
      >
        📹
      </button>
    </div>

    <!-- Incoming Call Modal -->
    <div v-if="incomingCall" class="call-modal incoming-call">
      <div class="call-modal-content">
        <div class="caller-info">
          <div class="caller-avatar">
            {{ getInitials(incomingCall.caller_name) }}
          </div>
          <div class="caller-details">
            <h3>{{ incomingCall.caller_name }}</h3>
            <p>Incoming {{ incomingCall.call_type }} call</p>
          </div>
        </div>
        <div class="call-actions">
          <button @click="acceptCall" class="call-action-btn accept">
            📞 Accept
          </button>
          <button @click="rejectCall" class="call-action-btn reject">
            📞 Decline
          </button>
        </div>
      </div>
    </div>

    <!-- Active Call Interface -->
    <div v-if="activeCall" class="call-modal active-call">
      <div class="call-modal-content">
        <div class="call-header">
          <div class="call-info">
            <h3>{{ activeCall.call_type === 'video' ? 'Video Call' : 'Audio Call' }}</h3>
            <p>{{ formatCallDuration(callDuration) }}</p>
          </div>
          <div class="call-status">
            <span :class="callStatus">{{ callStatus }}</span>
          </div>
        </div>

        <!-- Video Container -->
        <div v-if="activeCall.call_type === 'video'" class="video-container">
          <video
            ref="remoteVideo"
            class="remote-video"
            autoplay
            playsinline
          ></video>
          <video
            ref="localVideo"
            class="local-video"
            autoplay
            playsinline
            muted
          ></video>
        </div>

        <!-- Audio Visualization -->
        <div v-else class="audio-container">
          <div class="audio-visualization">
            <div class="audio-wave" :class="{ active: isAudioActive }">
              <span v-for="i in 5" :key="i" class="wave-bar"></span>
            </div>
          </div>
          <div class="participants">
            <div class="participant">
              <div class="participant-avatar">
                {{ getInitials(currentUser.display_name) }}
              </div>
              <span>You</span>
            </div>
            <div v-for="participant in callParticipants" :key="participant.user_id" class="participant">
              <div class="participant-avatar">
                {{ getInitials(participant.display_name) }}
              </div>
              <span>{{ participant.display_name }}</span>
            </div>
          </div>
        </div>

        <!-- Call Controls -->
        <div class="active-call-controls">
          <button
            @click="toggleMute"
            :class="{ active: isMuted }"
            class="control-btn mute-btn"
            title="Toggle Mute"
          >
            {{ isMuted ? '🔇' : '🎤' }}
          </button>
          
          <button
            v-if="activeCall.call_type === 'video'"
            @click="toggleVideo"
            :class="{ active: !isVideoEnabled }"
            class="control-btn video-btn"
            title="Toggle Video"
          >
            {{ isVideoEnabled ? '📹' : '📷' }}
          </button>
          
          <button
            @click="toggleSpeaker"
            :class="{ active: isSpeakerOn }"
            class="control-btn speaker-btn"
            title="Toggle Speaker"
          >
            {{ isSpeakerOn ? '🔊' : '🔈' }}
          </button>
          
          <button
            @click="endCall"
            class="control-btn end-call-btn"
            title="End Call"
          >
            📞
          </button>
        </div>

        <!-- Participants List -->
        <div v-if="callParticipants.length > 0" class="participants-list">
          <h4>Participants ({{ callParticipants.length + 1 }})</h4>
          <div class="participant-items">
            <div class="participant-item">
              <span>{{ currentUser.display_name }} (You)</span>
              <span class="participant-status">Connected</span>
            </div>
            <div
              v-for="participant in callParticipants"
              :key="participant.user_id"
              class="participant-item"
            >
              <span>{{ participant.display_name }}</span>
              <span class="participant-status" :class="participant.status">
                {{ participant.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import SimplePeer from 'simple-peer'

const props = defineProps({
  userId: {
    type: String,
    required: true
  },
  currentUser: {
    type: Object,
    required: true
  },
  roomId: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['call-started', 'call-ended', 'call-error'])

// Reactive data
const isInCall = ref(false)
const incomingCall = ref(null)
const activeCall = ref(null)
const callDuration = ref(0)
const callStatus = ref('connecting')
const callParticipants = ref([])

// Media controls
const isMuted = ref(false)
const isVideoEnabled = ref(true)
const isSpeakerOn = ref(false)
const isAudioActive = ref(false)

// WebRTC
const localStream = ref(null)
const remoteStream = ref(null)
const peer = ref(null)
const localVideo = ref(null)
const remoteVideo = ref(null)

// Call timer
const callTimer = ref(null)

// Methods
const initiateCall = async (callType) => {
  try {
    // Get user media
    const stream = await navigator.mediaDevices.getUserMedia({
      video: callType === 'video',
      audio: true
    })
    
    localStream.value = stream
    
    if (callType === 'video' && localVideo.value) {
      localVideo.value.srcObject = stream
    }

    // Create call session
    const response = await fetch('http://localhost:8000/calls/initiate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        call_type: callType,
        room_id: props.roomId,
        participant_ids: [] // Add specific participants if needed
      })
    })

    if (response.ok) {
      const data = await response.json()
      activeCall.value = data.call
      isInCall.value = true
      callStatus.value = 'calling'
      
      startCallTimer()
      setupWebRTC(true) // Initiator
      
      emit('call-started', data.call)
    }
  } catch (error) {
    console.error('Failed to initiate call:', error)
    emit('call-error', error.message)
  }
}

const acceptCall = async () => {
  try {
    // Get user media
    const stream = await navigator.mediaDevices.getUserMedia({
      video: incomingCall.value.call_type === 'video',
      audio: true
    })
    
    localStream.value = stream
    
    if (incomingCall.value.call_type === 'video' && localVideo.value) {
      localVideo.value.srcObject = stream
    }

    // Join call
    const response = await fetch(`http://localhost:8000/calls/${incomingCall.value.call_id}/join`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: props.userId })
    })

    if (response.ok) {
      activeCall.value = incomingCall.value
      incomingCall.value = null
      isInCall.value = true
      callStatus.value = 'connected'
      
      startCallTimer()
      setupWebRTC(false) // Not initiator
    }
  } catch (error) {
    console.error('Failed to accept call:', error)
    emit('call-error', error.message)
  }
}

const rejectCall = async () => {
  try {
    await fetch(`http://localhost:8000/calls/${incomingCall.value.call_id}/reject`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_id: props.userId })
    })
    
    incomingCall.value = null
  } catch (error) {
    console.error('Failed to reject call:', error)
  }
}

const endCall = async () => {
  try {
    if (activeCall.value) {
      await fetch(`http://localhost:8000/calls/${activeCall.value.id}/end`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: props.userId })
      })
    }
    
    cleanup()
    emit('call-ended')
  } catch (error) {
    console.error('Failed to end call:', error)
    cleanup()
  }
}

const setupWebRTC = (initiator) => {
  peer.value = new SimplePeer({
    initiator,
    trickle: false,
    stream: localStream.value
  })

  peer.value.on('signal', (data) => {
    // Send signaling data to server
    sendSignal(data)
  })

  peer.value.on('stream', (stream) => {
    remoteStream.value = stream
    if (remoteVideo.value) {
      remoteVideo.value.srcObject = stream
    }
    callStatus.value = 'connected'
  })

  peer.value.on('error', (error) => {
    console.error('WebRTC error:', error)
    emit('call-error', error.message)
  })

  peer.value.on('close', () => {
    cleanup()
  })
}

const sendSignal = async (signalData) => {
  try {
    await fetch(`http://localhost:8000/calls/${activeCall.value.id}/signal`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        signal_data: signalData,
        user_id: props.userId
      })
    })
  } catch (error) {
    console.error('Failed to send signal:', error)
  }
}

const toggleMute = () => {
  if (localStream.value) {
    const audioTrack = localStream.value.getAudioTracks()[0]
    if (audioTrack) {
      audioTrack.enabled = !audioTrack.enabled
      isMuted.value = !audioTrack.enabled
    }
  }
}

const toggleVideo = () => {
  if (localStream.value) {
    const videoTrack = localStream.value.getVideoTracks()[0]
    if (videoTrack) {
      videoTrack.enabled = !videoTrack.enabled
      isVideoEnabled.value = videoTrack.enabled
    }
  }
}

const toggleSpeaker = () => {
  isSpeakerOn.value = !isSpeakerOn.value
  // Note: Speaker control is limited in web browsers
  // This is more of a UI indicator
}

const startCallTimer = () => {
  callDuration.value = 0
  callTimer.value = setInterval(() => {
    callDuration.value++
  }, 1000)
}

const cleanup = () => {
  // Stop media streams
  if (localStream.value) {
    localStream.value.getTracks().forEach(track => track.stop())
    localStream.value = null
  }
  
  if (remoteStream.value) {
    remoteStream.value.getTracks().forEach(track => track.stop())
    remoteStream.value = null
  }

  // Close peer connection
  if (peer.value) {
    peer.value.destroy()
    peer.value = null
  }

  // Clear timer
  if (callTimer.value) {
    clearInterval(callTimer.value)
    callTimer.value = null
  }

  // Reset state
  activeCall.value = null
  incomingCall.value = null
  isInCall.value = false
  callDuration.value = 0
  callStatus.value = 'connecting'
  callParticipants.value = []
  isMuted.value = false
  isVideoEnabled.value = true
  isSpeakerOn.value = false
}

const formatCallDuration = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

// Handle incoming call invitations
const handleCallInvitation = (callData) => {
  incomingCall.value = callData
}

// Handle WebRTC signaling
const handleSignal = (signalData) => {
  if (peer.value) {
    peer.value.signal(signalData.signal_data)
  }
}

// Lifecycle
onMounted(() => {
  // Set up audio activity detection
  if (localStream.value) {
    // Audio activity detection would go here
    // This is a simplified version
    setInterval(() => {
      isAudioActive.value = !isMuted.value && Math.random() > 0.7
    }, 500)
  }
})

onUnmounted(() => {
  cleanup()
})

// Expose methods for parent component
defineExpose({
  handleCallInvitation,
  handleSignal,
  cleanup
})
</script>

<style scoped>
.call-interface {
  position: relative;
}

.call-controls {
  display: flex;
  gap: 8px;
}

.call-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.2s;
}

.call-btn:hover:not(:disabled) {
  background: #218838;
  transform: translateY(-1px);
}

.call-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.video-call {
  background: #007bff;
}

.video-call:hover:not(:disabled) {
  background: #0056b3;
}

.call-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.call-modal-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
}

.incoming-call .call-modal-content {
  text-align: center;
  max-width: 400px;
}

.active-call .call-modal-content {
  max-width: 800px;
  min-height: 500px;
}

.caller-info {
  margin-bottom: 24px;
}

.caller-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #007bff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 600;
  margin: 0 auto 16px;
}

.caller-details h3 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.caller-details p {
  margin: 0;
  color: #666;
  font-size: 16px;
}

.call-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.call-action-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.accept {
  background: #28a745;
  color: white;
}

.accept:hover {
  background: #218838;
}

.reject {
  background: #dc3545;
  color: white;
}

.reject:hover {
  background: #c82333;
}

.call-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.call-info h3 {
  margin: 0 0 4px 0;
  font-size: 20px;
  color: #333;
}

.call-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.call-status span {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.call-status .connecting {
  background: #fff3cd;
  color: #856404;
}

.call-status .connected {
  background: #d4edda;
  color: #155724;
}

.call-status .calling {
  background: #cce7ff;
  color: #004085;
}

.video-container {
  position: relative;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
  height: 400px;
}

.remote-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.local-video {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 150px;
  height: 100px;
  border-radius: 8px;
  border: 2px solid white;
  object-fit: cover;
}

.audio-container {
  text-align: center;
  padding: 40px 20px;
}

.audio-visualization {
  margin-bottom: 40px;
}

.audio-wave {
  display: flex;
  justify-content: center;
  align-items: end;
  gap: 4px;
  height: 60px;
}

.wave-bar {
  width: 4px;
  background: #007bff;
  border-radius: 2px;
  transition: height 0.3s ease;
  height: 10px;
}

.audio-wave.active .wave-bar {
  animation: wave 1s ease-in-out infinite;
}

.audio-wave.active .wave-bar:nth-child(2) {
  animation-delay: 0.1s;
}

.audio-wave.active .wave-bar:nth-child(3) {
  animation-delay: 0.2s;
}

.audio-wave.active .wave-bar:nth-child(4) {
  animation-delay: 0.3s;
}

.audio-wave.active .wave-bar:nth-child(5) {
  animation-delay: 0.4s;
}

@keyframes wave {
  0%, 100% { height: 10px; }
  50% { height: 40px; }
}

.participants {
  display: flex;
  justify-content: center;
  gap: 24px;
}

.participant {
  text-align: center;
}

.participant-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #6c757d;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  margin: 0 auto 8px;
}

.participant span {
  font-size: 14px;
  color: #666;
}

.active-call-controls {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin: 20px 0;
}

.control-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: none;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s;
  background: #f8f9fa;
  color: #333;
}

.control-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.control-btn.active {
  background: #dc3545;
  color: white;
}

.end-call-btn {
  background: #dc3545;
  color: white;
}

.end-call-btn:hover {
  background: #c82333;
}

.participants-list {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
}

.participants-list h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #666;
  text-transform: uppercase;
}

.participant-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.participant-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 6px;
}

.participant-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  text-transform: uppercase;
  font-weight: 600;
}

.participant-status.connected {
  background: #d4edda;
  color: #155724;
}

.participant-status.invited {
  background: #fff3cd;
  color: #856404;
}

.participant-status.left {
  background: #f8d7da;
  color: #721c24;
}
</style>
