const { 
  SolclientFactory, 
  SDTField,
  SDTFieldType,
  Session, 
  StatType,
  SessionEventCode,
  TransportProtocol 
} = solace;
const { 
  createSession, 
  createTopicDestination, 
  createMessage,
} = SolclientFactory;
const {
  getCurrentService
} = (SolaceCloud || {});

const app = new Vue({
  
  el: '#app',
  
  data: {
    tabs: {
      session: {
        active: true,
        form: {
          url: 'ws://localhost',
          userName: 'default',
          password: 'secret',
          vpnName: 'default',
          transportProtocol: TransportProtocol.HTTP_BINARY_STREAMING,
          button: {
            connect: 'Connect',
            disconnect: 'Disconnect'
          }
        },
        status: {
          show: false,
          message: ''
        }
      },
      publish: {
        form: {
          topic: 'topic/try/me',
          message: 'Hello world!',
          format: 'binaryAttachment',
          button: {
            publish: 'Publish'
          }
        },
        status: {
          show: false,
          message: ''
        }
      }
    },
    
    connected: false,
    session: null,
    pendingSession: null,
    showAdvancedSettings: false
  },
  
  methods: {
    
    // Initialize the Solace API factory.
    init() {
      SolclientFactory.init({
        profile: SolclientFactory.profiles.version7
      });
      // If embedded in Solace Cloud (as a demo), ask the console for service credentials.
      getCurrentService && getCurrentService((r) => app.setSessionCredentials(r.data.service));
    },
    
    // Reset the application state.
    reset() {
      this.session.dispose();
      this.session = null;
      this.connected = false;
    },
    
    // Connect the session.
    connect() {
      if (this.session) this.reset();
      
      // Create a session with the given session properties
      try {
        this.session = createSession(this.tabs.session.form);
      } catch (ex) {
        this.setStatus('session', 'Error creating session: ' + ex.message);
        return;
      }
      
      this.session.on(SessionEventCode.UP_NOTICE, () => {
        this.sessionRequestCompleted();
        this.connected = true;
        this.setActiveTab('publish');
      });
      this.session.on(SessionEventCode.DISCONNECTED, () => {
        this.sessionRequestCompleted();
        this.reset();
      });
      this.session.on(SessionEventCode.DOWN_ERROR, (...args) => {
        console.log('DOWN_ERROR', args);
        this.setStatus('session', 'Session down with error ' + event);
        this.reset();
      });
 
      // Connect the session
      this.showSessionRequestPending();
      try {
        this.session.connect();      
      } catch (ex) {
        this.setStatus('session', 'Error connecting session: ' + ex.message);
        this.reset();
      }      
    },
    
    // Disconnect the session.
    disconnect() {
      if (!this.session) return;
      this.showSessionRequestPending();
      this.session.disconnect();
    },
    
    // Publish a message.
    // It is safe to publish arbitrary data, including text in the message's 
    // binaryAttachment, but using an SDT String field adds metadata to help 
    // identify the message content.
    publish() {
      const { session } = this;
      const { form } = this.tabs.publish;
      const message = createMessage();
      if (form.format == 'binaryAttachment') {
        message.setBinaryAttachment(form.message);
      } else {
        message.setSdtContainer(SDTField.create(SDTFieldType.STRING, form.message));
      }
      
      try {
        message.setDestination(createTopicDestination(form.topic));
        session.send(message);
      } catch (ex) {
        this.setStatus('publish', 'Publish error: ' + ex.message);      
        return;
      }
      this.setStatus('publish', session.getStat(StatType.TX_DIRECT_MSGS) + ' message(s) published');
    },
    
    // Pop up a status update.
    setStatus(type, message) {
      const statusNode = this.tabs[type].status;
      Object.assign(statusNode, {
        show: true,
        message
      });
      this.sessionRequestCompleted();
    },
    
    showSessionRequestPending() {
      this.sessionRequestPending = true;
    },
    
    sessionRequestCompleted() {
      this.sessionRequestPending = false;
    },
    
    // Set the active (displayed) UI tab.
    setActiveTab(selection) {
      Object.keys(this.tabs).forEach(tabName => {
        this.tabs[tabName].active = (tabName === selection);
      });
    },
    
    // toggle the advanced settings
    toggleAdvancedSettings() {
      this.showAdvancedSettings = !this.showAdvancedSettings;
    },
    
    // Accept external session properties.
    setSessionCredentials(properties) {
      Object.assign(this.tabs.session.form, properties);
    }
    
  },
  
  mounted() {
    document.getElementById('vue-loading').remove();
    this.init();
  }
  
});