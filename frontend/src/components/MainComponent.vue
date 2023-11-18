<template>
    <div class="main-container">
        Hello world
        <div class="top-right-buttons">
            <!-- <Button severity="info" rounded v-if="!isConnected" id="connectWallet" class="connect-button" @click="enableEthereum" label="Connect wallet" />
            <Button severity="info" rounded v-else id="disconnectWallet" class="disconnect-button" :label=shortAddress(currentAccount) /> -->
        </div>
    </div>
</template>


<script>
// import { ref, onMounted } from 'vue';
// import tokensInfo from '@/info/tokensInfo.json';
// import { shortAddress, formatNumber } from '@/helpers/helpers.js';
// import { signPermit } from '@/signatures/permit.js';
// import { signMetaTransaction } from '@/signatures/metaTransaction.js';
// import InputText from 'primevue/inputtext';
// import Button from 'primevue/button';
// import ProgressSpinner from 'primevue/progressspinner';
// import { getChains, 
//          getBalances, 
//          getRoutes, 
//          getRouterInfo, 
//          getTokenInfo, 
//          getBridgesInfo,
//          sendTransaction} from '@/api/index.js'
export default {
    components: {
    //   InputText,
    //   Button,
    //   ProgressSpinner
    },
    name: 'MainComponent',
}
</script>