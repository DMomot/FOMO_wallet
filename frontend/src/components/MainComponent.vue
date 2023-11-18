<template>
    <div class="main-container">
        <div v-if="screen=='search'" class="main-container-search">
            <div class="main-header">
                <div class="main-title">Fomogotchi</div>
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
            <div class="main-total-container">
                <div class="total-info-block">
                    <div class="total-info-title">Total Value</div>
                    <div class="total-info-value">{{ formatValue(totalFomoValues.totalValue) }} $</div>
                </div>
                <div class="total-info-block">
                    <div class="total-info-title">Total Unrealized Profit by 1 month</div>
                    <div class="total-info-value">-{{ formatValue(totalFomoValues.totalUP) }} $</div>
                </div>
                <div class="total-info-block">
                    <div class="total-info-title">Total Unrealized APR</div>
                    <div class="total-info-value">[Значение]</div>
                </div>
            </div>
            <div class="tokens-header">
                <h1>Tokens</h1>
            </div>
            <div class="token-list">
                <div class="token-item">
                    <span class="token-img"> </span>
                    <span class="token-name">Name</span>
                    <span class="token-amount">Amount</span>
                    <span class="token-price">Price</span>
                    <span class="token-value">Value</span>
                    <span class="token-pnl">Unreal. revenue</span>
                    <span class="token-roi">APY</span>
                </div>
                <div v-for="token in tokens"
                    :key="(token.address, token.chain_id)"
                    class="token-item"
                    @click="showModal(token)">
                    <div class="img-container">
                        <img v-if="token.logo_url" :src=token.logo_url :alt=key class="token-img">
                        <img v-else :src=template_logo :alt=key class="token-img">
                        <img :src=chainsLogo[token.chain_id] :alt=key class="chain-img">
                    </div>
                    <span class="token-name">{{ token.name }}</span>
                    <span class="token-amount">
                        {{ token.amount.toFixed(4) }} {{ token.symbol }}
                    </span>
                    <span class="token-price">
                        {{ token.price.toFixed(4)  }}
                    </span>
                    <span class="token-value">
                        {{ formatValue(token.amount * token.price) }} $
                    </span>
                    <span v-if="token.fomo" class="token-pnl">
                        {{formatValue(token.fomo[0].unrealized_value) }} $
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
                </div>
                <Dialog v-model:visible="dialogVisible" modal :style="{ width: '50vw' }" :header="'Unrealized rewards'">
                    <div class="dialog-container">
                        <table class="data-table">
                        <thead>
                            <tr>
                                <th>Chain</th>
                                <th>Protocol Name</th>
                                <th>Token Name</th>
                                <th>APY</th>
                                <th>Unrealized Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in dialogData.fomo" :key="item.protocol_name">
                                <td>{{ item.chain_id }}</td>
                                <td>{{ item.protocol_name }}</td>
                                <td>{{ dialogData.name }}</td>
                                <td>{{ formatValue(item.apy) }}</td>
                                <td>{{ formatValue(item.unrealized_value) }} $</td>
                            </tr>
                        </tbody>
                        </table>
                    </div>
                    <div>
                        {{ dialogData }}
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
import { ref } from 'vue';
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

        const template_logo = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIsbGx31Hoow8Inq8Tr0TjAsyU4nVkxB4pEGNmPfFfxQ&s'
        let searchQuery = ref('0xd470055c6189b921c4d44b3d277ad868f79c0f75')
        let screen = ref('search')
        let tokens = ref([])
        let dialogVisible = ref(false);
        let dialogData = ref({});
        let currentAddress = ref('')
        let isLoading = ref(false);
        let totalFomoValues = ref({})


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