<template>
    <div class="main-container">
        <div v-if="screen=='search'" class="main-container-search">
            <div class="main-header">
                <img src="/logo.png" alt="logo" class="main-logo" style="border-radius: 50%; width: 10rem">
                <div class="main-title">FomoGotchi</div>
            </div>
            <div class="search-container">
                <InputText type="text" v-model="searchQuery" @keyup.enter="FOMOSearch" placeholder="Enter address" class="search-input"/>
                <Button @click="FOMOSearch" class="search-button" label="Search"/>
            </div>
        </div>
        <div v-else class="main-container-result">
            <div class="search-container-header">
                <InputText type="text" v-model="searchQuery" @keyup.enter="FOMOSearch" placeholder="Enter address" class="search-input"/>
                <Button @click="FOMOSearch" class="search-button" label="Search"/>
            </div>
            <div class="address-header">
                <div class="address-title">Address {{ currentAddress }}</div>
            </div>
          <div class="token-header-container">
                <div class="images-container">
                    <img :src="chainsLogo[1]" class="chain_img_list" alt="Token 1">
                    <img :src="chainsLogo[137]" alt="Token 2">
                    <img :src="chainsLogo[42161]" alt="Token 3">
                    <img :src="chainsLogo[100]" alt="Token 4">
                </div>
            </div>
            <div class="main-total-container">
                <div class="total-info-block">
                    <div class="total-info-title">Total Value</div>
                    <div class="total-info-value">{{ formatValue(totalFomoValues.totalValue) }} $</div>
                </div>
                <div class="total-info-block">
                    <div class="total-info-title-ul">You lost by 1 year</div>
                    <div class="total-info-value-ul">{{ formatValue(totalFomoValues.totalUP) }} $</div>
                </div>
                <div class="total-info-block">
                    <div class="total-info-title">Total Unrealized APR</div>
                    <div class="total-info-value">{{ formatValue(100 * totalFomoValues.totalUP/totalFomoValues.totalValue) }} %</div>
                </div>
            </div>
            <div class="token-list">
                <div class="token-item-header">
                    <span class="token-img"> </span>
                    <span class="token-name">Name</span>
                    <span class="token-amount">Amount</span>
                    <span class="token-value">Value</span>
                    <span class="token-protocol">Protocol</span>
                    <span class="token-pnl">You lost 1Y</span>
                    <span class="token-roi">APY 1Y</span>
                    <span class="token-invest"></span>
                </div>
                <div v-for="token in tokens"
                    :key="(token.address, token.chain_id)"
                    class="token-item"
                    @click="showModal(token)">
                    <div class="img-container">
                        <img v-if="token.logo_url" :src=token.logo_url class="token-img">
                        <img v-else :src=template_logo class="token-img">
                        <img :src=chainsLogo[token.chain_id] class="chain-img">
                    </div>
                    <span class="token-name">{{ token.name }}</span>
                    <span class="token-amount">
                        {{ token.amount.toFixed(4) }} {{ token.symbol }}
                    </span>
                    <span class="token-value">
                        {{ formatValue(token.amount * token.price) }} $
                    </span>
                    <span v-if="token.fomo" class="token-protocol">
                        <img :src=token.fomo[0].logo_url class="protocol-img">
                        {{ token.fomo[0].protocol_name }}
                    </span>
                    <span v-else class="token-protocol">
                        No rewards
                    </span>
                    <span v-if="token.fomo" class="token-pnl">
                        {{ formatValue(token.fomo[0].unrealized_value) }} $
                    </span>
                    <span v-else class="token-pnl">
                        0
                    </span>
                    <span v-if="token.fomo" class="token-roi">
                        {{ (100 * token.fomo[0].apy).toFixed(2) }} %
                    </span>
                    <span v-else class="token-roi">
                        0
                    </span>
                    <span v-if="token.fomo" class="token-roi">
                        <Button label="Invest" class="p-button-raised p-button-rounded p-button-success" />
                    </span> 
                    <span v-else class="token-invest">
                        <Button label="Invest" class="p-button-raised p-button-rounded p-button-disabled" />
                    </span>
                </div>
                <Dialog v-model:visible="dialogVisible" modal :style="{ width: '50vw' }" :header="'Unrealized rewards'">
                    <div class="dialog-container">
                        <table class="data-table">
                        <thead>
                            <tr>
                                <th>Chain</th>
                                <th>Protocol Name</th>
                                <th>Token Name</th>
                                <th>APY 1Y</th>
                                <th>You lost 1Y</th>
                                <th>Invest</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in dialogData.fomo" :key="item.protocol_name">
                                <td>{{ item.chain_id }}</td>
                                <td>{{ item.protocol_name }}</td>
                                <td>
                                    <div class="protocol-img-name">
                                    <img :src=item.logo_url alt="logo" class="protocol-img-dialog">
                                    {{ item.protocol_name }}
                                    </div>
                                </td>
                                <td>{{ (100 * item.apy).toFixed(2) }}%</td>
                                <td>{{ formatValue(item.unrealized_value) }} $</td>
                                <td><Button label="Invest" class="p-button-raised p-button-rounded p-button-success" @click="openLink(item.project_url)"/></td>
                            </tr>
                        </tbody>
                        </table>
                    </div>
                </Dialog>
            </div>
        </div>
        <div v-if="isLoading" class="custom-modal">
            <div class="spinner-container">
                <ProgressSpinner />
            </div>
        </div>
    </div>
</template>


<script>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import chainsLogo from '@/helpers/chainsLogo.json'
import ProgressSpinner from 'primevue/progressspinner';

import { checkAddress, calculateTotalValues, formatValue } from '@/helpers/index.js'
import { getFomoVibe } from '@/api/index.js'

export default {
    components: {
      ProgressSpinner,
      Dialog,
      InputText,
      Button,
    },
    name: 'MainComponent',
    
    setup() {

        const route = useRoute();

        let currentAddress = ref('');
        let searchQuery = ref('')
        

        watch(() => route.params, (newParams) => {
            if (newParams.address) {
                searchQuery.value = newParams.address;
                FOMOSearch();
            }
        }, { immediate: true });

        const template_logo = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIsbGx31Hoow8Inq8Tr0TjAsyU4nVkxB4pEGNmPfFfxQ&s'
        let screen = ref('search')
        let tokens = ref([])
        let dialogVisible = ref(false);
        let dialogData = ref({});
        let isLoading = ref(false);
        let totalFomoValues = ref({})

        const openLink = (link) =>{
            window.open(link, '_blank');
        }



        const FOMOSearch = async () => {
            isLoading.value = true;
            const address = await checkAddress(searchQuery.value)
            tokens.value = await getFomoVibe(address)
            currentAddress.value = searchQuery.value
            searchQuery.value = ''
            screen.value = 'result'
            totalFomoValues.value = calculateTotalValues(tokens.value)
            isLoading.value = false;
        }

        const showModal = (token) => {
            dialogData.value = token
            dialogVisible.value = true;
        }

        return {
            template_logo,
            openLink,
            currentAddress,
            FOMOSearch,
            showModal,
            dialogVisible,
            dialogData,
            chainsLogo,
            tokens,
            totalFomoValues,
            formatValue,
            ProgressSpinner,
            searchQuery,
            screen,
            isLoading
        }
    }
}
</script>