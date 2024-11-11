import React, { useState, useEffect, useRef } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Animated,
  Easing,
} from "react-native";
import { Audio } from "expo-av";
import { Ionicons } from "@expo/vector-icons";

export default function AudioCommandAssistant() {
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [messages, setMessages] = useState<
    Array<{ text: string; sender: "user" | "ai" }>
  >([]);

  const spinValue = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    return () => {
      if (recording) {
        recording.stopAndUnloadAsync();
      }
      if (sound) {
        sound.unloadAsync();
      }
    };
  }, []);

  useEffect(() => {
    if (isSending) {
      Animated.loop(
        Animated.timing(spinValue, {
          toValue: 1,
          duration: 2000,
          easing: Easing.linear,
          useNativeDriver: true,
        })
      ).start();
    } else {
      spinValue.setValue(0);
    }
  }, [isSending]);

  const spin = spinValue.interpolate({
    inputRange: [0, 1],
    outputRange: ["0deg", "360deg"],
  });

  async function startRecording() {
    try {
      await Audio.requestPermissionsAsync();
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
      setIsRecording(true);
    } catch (err) {
      console.error("Failed to start recording", err);
      addMessage("Failed to start recording. Please try again.", "ai");
    }
  }

  async function stopRecording() {
    if (!recording) return;

    setIsRecording(false);
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();
    setRecording(null);

    if (uri) {
      console.log("Recording stopped and saved at", uri);
      addMessage("Audio command recorded", "ai");
      await sendAudioToBackend(uri);
    }
  }

  async function sendAudioToBackend(uri: string) {
    setIsSending(true);
    addMessage("Processing your audio command...", "ai");

    try {
      // get the audio data from the file
      // get file from file system
      const file = await fetch(uri);
      const fileBlob = await file.blob();
      const fileReader = new FileReader();
      const audio_data = new Promise((resolve, reject) => {
        fileReader.onload = () => {
          resolve(fileReader.result);
        };
        fileReader.onerror = reject;
        fileReader.readAsDataURL(fileBlob);
      });

      const backendResponse = await fetch(
        "http://192.168.139.47:8000/predict",
        {
          method: "POST",
          body: JSON.stringify({
            audio_data: await audio_data,
          }),
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!backendResponse.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await backendResponse.json();

      if (data.error) {
        addMessage(data.error, "ai");
      }

      if (data.audio_file_url && data.answer) {
        addMessage(data.answer, "ai");
        await playAudioResponse(
          "http://192.168.139.47:8000" + data.audio_file_url
        );
      } else {
        addMessage("Received a response, but no audio was provided.", "ai");
      }
    } catch (error) {
      console.error("Error sending audio to backend:", error);
      addMessage(
        "Sorry, there was an error processing your command. Please try again.",
        "ai"
      );
    } finally {
      setIsSending(false);
    }
  }

  async function playAudioResponse(uri: string) {
    try {
      const res = await fetch(uri);

      if (!res.ok) {
        throw new Error("Network response was not ok");
      }

      const audioBlob = await res.blob();
      const audioBase64 = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
          resolve(reader.result);
        };
        reader.onerror = reject;
        reader.readAsDataURL(audioBlob);
      });

      const audioUri = `data:audio/mp3;base64,${audioBase64}`;
      const { sound: newSound } = await Audio.Sound.createAsync({
        uri: audioUri,
      });
      setSound(newSound);

      addMessage("Playing audio response...", "ai");
      setIsPlaying(true);
      await newSound.playAsync();
      newSound.setOnPlaybackStatusUpdate((status) => {
        if (status.isLoaded && status.didJustFinish) {
          setIsPlaying(false);
        }
      });
    } catch (error) {
      console.error("Error playing audio:", error);
      addMessage("Failed to play audio response. Please try again.", "ai");
    }
  }

  const addMessage = (text: string, sender: "user" | "ai") => {
    setMessages((prevMessages) => [...prevMessages, { text, sender }]);
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
      addMessage("Audio command sent", "user");
    } else {
      startRecording();
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>SandalQuest Audio Assistant</Text>
      </View>
      <ScrollView
        style={styles.messageArea}
        contentContainerStyle={styles.messageContainer}
      >
        {messages.map((message, index) => (
          <View
            key={index}
            style={[
              styles.messageBubble,
              message.sender === "user" ? styles.userBubble : styles.aiBubble,
            ]}
          >
            <Text
              style={[
                styles.messageText,
                message.sender === "ai" ? styles.aiMessageText : null,
              ]}
            >
              {message.text}
            </Text>
          </View>
        ))}
        {isSending && (
          <View style={styles.loadingContainer}>
            <Animated.View style={{ transform: [{ rotate: spin }] }}>
              <Ionicons name="reload-outline" size={40} color="#8B4513" />
            </Animated.View>
            <Text style={styles.loadingText}>Processing audio...</Text>
          </View>
        )}
      </ScrollView>
      <View style={styles.footer}>
        <TouchableOpacity
          style={[styles.micButton, isRecording && styles.micButtonActive]}
          onPress={toggleRecording}
          disabled={isSending || isPlaying}
        >
          <Ionicons
            name={isRecording ? "stop" : "mic"}
            size={40}
            color="white"
          />
        </TouchableOpacity>
        <Text style={styles.footerText}>
          {isRecording ? "Recording... Tap to stop" : "Tap to record command"}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF8DC",
  },
  header: {
    padding: 20,
    backgroundColor: "#8B4513",
  },
  headerText: {
    color: "white",
    fontSize: 24,
    fontWeight: "bold",
  },
  messageArea: {
    flex: 1,
  },
  messageContainer: {
    padding: 15,
  },
  messageBubble: {
    maxWidth: "80%",
    padding: 12,
    borderRadius: 20,
    marginBottom: 10,
  },
  userBubble: {
    alignSelf: "flex-end",
    backgroundColor: "#DEB887",
  },
  aiBubble: {
    alignSelf: "flex-start",
    backgroundColor: "#8B4513",
  },
  messageText: {
    fontSize: 16,
  },
  aiMessageText: {
    color: "white",
  },
  footer: {
    alignItems: "center",
    paddingVertical: 20,
  },
  micButton: {
    backgroundColor: "#8B4513",
    width: 80,
    height: 80,
    borderRadius: 40,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 10,
  },
  micButtonActive: {
    backgroundColor: "#CD853F",
  },
  footerText: {
    color: "#8B4513",
    fontSize: 16,
  },
  loadingContainer: {
    alignItems: "center",
    marginTop: 20,
  },
  loadingText: {
    marginTop: 10,
    color: "#8B4513",
    fontSize: 16,
  },
});
