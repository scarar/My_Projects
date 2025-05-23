<?
/* define('DB_HOST', 'localhost');
define('DB_USERNAME', 'db_username');
define('DB_PASSWORD', 'db_password');
define('DB_NAME', 'db_username'); */
?>
<?php
// Database connection test script
error_reporting(E_ALL);
ini_set('display_errors', 1);

define('DB_HOST', 'localhost');
define('DB_USERNAME', 'db_username');
define('DB_PASSWORD', 'password');
define('DB_NAME', 'db_username');

echo "<h2>Database Connection Test</h2>";
echo "<hr>";

// Show configuration first
echo "<h3>Configuration Check</h3>";
echo "Host: " . DB_HOST . "<br>";
echo "Username: " . DB_USERNAME . "<br>";
echo "Database: " . DB_NAME . "<br>";
echo "PHP Version: " . phpversion() . "<br>";
echo "MySQLi Extension: " . (extension_loaded('mysqli') ? '✅ Loaded' : '❌ Not loaded') . "<br>";
echo "<hr>";

// Test 1: Basic connection
echo "<h3>Test 1: Basic Connection</h3>";
echo "Attempting to connect...<br>";

$conn = @mysqli_connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if (!$conn) {
    $error = mysqli_connect_error();
    echo "<span style='color: red; font-weight: bold;'>❌ CONNECTION FAILED!</span><br>";
    echo "<span style='color: red;'>Error: " . $error . "</span><br>";
    echo "<span style='color: red;'>Error Number: " . mysqli_connect_errno() . "</span><br>";
    
    echo "<hr>";
    echo "<h3>Connection failed - troubleshooting tips</h3>";
    echo "<p>Please check:</p>";
    echo "<ul>";
    echo "<li>MySQL/MariaDB server is running</li>";
    echo "<li>Database credentials are correct</li>";
    echo "<li>Database '" . DB_NAME . "' exists</li>";
    echo "<li>User '" . DB_USERNAME . "' has access to the database</li>";
    echo "</ul>";
    
} else {
    echo "<span style='color: green; font-weight: bold;'>✅ CONNECTION SUCCESSFUL!</span><br>";
    echo "<span style='color: green;'>Connected to database successfully!</span><br>";
    
    // Test 2: Connection details
    echo "<h3>Test 2: Connection Details</h3>";
    echo "MySQL Version: " . mysqli_get_server_info($conn) . "<br>";
    echo "Client Version: " . mysqli_get_client_info() . "<br>";

    // Test 3: Database selection
    echo "<h3>Test 3: Database Selection</h3>";
    if (mysqli_select_db($conn, DB_NAME)) {
        echo "<span style='color: green;'>✅ Database '" . DB_NAME . "' selected successfully</span><br>";
    } else {
        echo "<span style='color: red;'>❌ Failed to select database: " . mysqli_error($conn) . "</span><br>";
    }

    // Test 4: Simple query test
    echo "<h3>Test 4: Query Test</h3>";
    $result = mysqli_query($conn, "SELECT 1 as test_value");
    if ($result) {
        $row = mysqli_fetch_assoc($result);
        echo "<span style='color: green;'>✅ Test query successful. Result: " . $row['test_value'] . "</span><br>";
        mysqli_free_result($result);
    } else {
        echo "<span style='color: red;'>❌ Test query failed: " . mysqli_error($conn) . "</span><br>";
    }

    // Test 5: Show tables (if any exist)
    echo "<h3>Test 5: Database Tables</h3>";
    $result = mysqli_query($conn, "SHOW TABLES");
    if ($result) {
        $table_count = mysqli_num_rows($result);
        echo "Number of tables in database: " . $table_count . "<br>";
        
        if ($table_count > 0) {
            echo "Tables:<br>";
            while ($row = mysqli_fetch_array($result)) {
                echo "- " . $row[0] . "<br>";
            }
        } else {
            echo "<span style='color: orange;'>⚠️ No tables found in database</span><br>";
        }
        mysqli_free_result($result);
    } else {
        echo "<span style='color: red;'>❌ Failed to show tables: " . mysqli_error($conn) . "</span><br>";
    }

    // Test 6: Connection status
    echo "<h3>Test 6: Connection Status</h3>";
    
    // Check PHP version for mysqli_ping compatibility
    if (version_compare(PHP_VERSION, '8.4.0', '<')) {
        // Use mysqli_ping for PHP versions below 8.4
        if (mysqli_ping($conn)) {
            echo "<span style='color: green;'>✅ Connection is still alive (verified with ping)</span><br>";
        } else {
            echo "<span style='color: red;'>❌ Connection lost</span><br>";
        }
    } else {
        // For PHP 8.4+, use an alternative method to check connection
        $test_query = mysqli_query($conn, "SELECT 1");
        if ($test_query) {
            echo "<span style='color: green;'>✅ Connection is still alive (verified with query)</span><br>";
            mysqli_free_result($test_query);
        } else {
            echo "<span style='color: red;'>❌ Connection appears to be lost</span><br>";
        }
    }

    // Close connection
    mysqli_close($conn);
    echo "<h3>Connection closed successfully</h3>";
}

echo "<hr>";
echo "<p><strong>Test completed at: " . date('Y-m-d H:i:s') . "</strong></p>";
?>
