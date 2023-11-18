<template>
    <div class="main-container">
        <div v-if="screen=='search'" class="main-container-search">
            <div class="main-header">
                <div class="main-title">FOMO wallet</div>
            </div>
            <div class="search-container">
                <InputText type="text" v-model="searchQuery" @keyup.enter="performSearch" placeholder="Enter address" class="search-input"/>
                <Button @click="performSearch" class="search-button" label="Search"/>
            </div>
        </div>
        <div v-else class="main-container-result">
            
        </div>
    </div>
</template>


<script>
import { ref } from 'vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
// import ProgressSpinner from 'primevue/progressspinner';
import { getAllBalances } from '@/helpers/index.js'
export default {
    components: {
      InputText,
      Button,
    },
    name: 'MainComponent',
    setup() {
        let searchQuery = ref('0xd470055c6189b921c4d44b3d277ad868f79c0f75')
        let screen = ref('search')

        const performSearch = async () => {
            const balances = await getAllBalances(searchQuery.value)
            console.log(balances)
            screen.value = 'result'
        }

        return {
            performSearch,
            searchQuery,
            screen
        }
    }
}


</script>