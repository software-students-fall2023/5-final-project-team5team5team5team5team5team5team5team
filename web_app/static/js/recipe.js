const init = () => {
    const tabs = document.querySelectorAll('a.tab')
    let activeTab = document.querySelector('a.tab-selected')
    for (const t of tabs) {
        t.addEventListener('click', evt => {
            evt.preventDefault()
            activeTab.classList.remove('tab-selected')
            document.querySelector(activeTab.getAttribute('tab-target')).style.display = 'none'
            t.classList.add('tab-selected')
            activeTab = t
            document.querySelector(activeTab.getAttribute('tab-target')).style.display = 'block'
        })
    }
};

if (document.readyState !== "loading") init()
else window.addEventListener("load", init)